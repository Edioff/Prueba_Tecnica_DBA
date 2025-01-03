CREATE OR REPLACE FUNCTION detectar_apuestas_identicas()
RETURNS TRIGGER AS $$
DECLARE
    total_apuestas INT;
BEGIN
    -- Verificar si ya existe un registro sospechoso reciente para evitar inserciones repetidas
    IF NOT EXISTS (
        SELECT 1 FROM patrones_sospechosos_5_min 
        WHERE usuario_id = NEW.usuario_id
        AND evento_id = NEW.evento_id
        AND monto_apostado = NEW.monto_apostado
        AND cuota = NEW.cuota
        AND detectado_en >= NOW() - INTERVAL '5 minutes'
    ) THEN
        -- Contar apuestas idénticas en los últimos 5 minutos
        SELECT COUNT(*)
        INTO total_apuestas
        FROM Apuestas
        WHERE evento_id = NEW.evento_id
          AND monto_apostado = NEW.monto_apostado
          AND cuota = NEW.cuota
          AND timestamp BETWEEN NOW() - INTERVAL '5 minutes' AND NOW();

        -- Si hay más de 20 apuestas idénticas en el intervalo, registrar el patrón
        IF total_apuestas > 20 THEN
            INSERT INTO patrones_sospechosos_5_min (
                tipo_patron,
                usuario_id,
                evento_id,
                monto_apostado,
                cuota,
                detectado_en,
                total_apuestas
            ) VALUES (
                'Apuestas Idénticas',
                NEW.usuario_id,
                NEW.evento_id,
                NEW.monto_apostado,
                NEW.cuota,
                CURRENT_TIMESTAMP,
                total_apuestas
            );
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_apuestas_identicas ON Apuestas;

CREATE TRIGGER trigger_apuestas_identicas
AFTER INSERT ON Apuestas
FOR EACH ROW
EXECUTE FUNCTION detectar_apuestas_identicas();
