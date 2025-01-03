CREATE OR REPLACE FUNCTION detectar_apuestas_sospechosas()
RETURNS TRIGGER AS $$
BEGIN
    IF (
        SELECT COUNT(*)
        FROM Apuestas
        WHERE usuario_id = NEW.usuario_id
          AND timestamp >= NOW() - INTERVAL '10 minutes'
    ) > 50 THEN
        INSERT INTO patrones_sospechosos_10_min (
            usuario_id, 
            total_apuestas, 
            inicio_intervalo, 
            fin_intervalo, 
            tipo_patron
        )
        SELECT 
            NEW.usuario_id,
            COUNT(*) AS total_apuestas,
            MIN(timestamp) AS inicio_intervalo,
            MAX(timestamp) AS fin_intervalo,
            'Apuestas en 10 minutos'
        FROM Apuestas
        WHERE usuario_id = NEW.usuario_id
          AND timestamp >= NOW() - INTERVAL '10 minutes';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear el trigger
CREATE TRIGGER trigger_apuestas_sospechosas
AFTER INSERT ON Apuestas
FOR EACH ROW
EXECUTE FUNCTION detectar_apuestas_sospechosas();
