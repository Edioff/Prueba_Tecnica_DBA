-- Patrón 2.2: Más de 20 apuestas idénticas en 5 minutos
-- Nota: Este script requiere los siguientes índices que estan el el archivo crear_indices:

-- Crear índice en las columnas necesarias
--CREATE INDEX idx_apuestas_identicas ON Apuestas (evento_id, monto_apostado, cuota, timestamp); 

WITH ApuestasAgrupadas AS (
    SELECT
        evento_id,
        monto_apostado,
        cuota,
        COUNT(*) AS total_apuestas,
        MIN(timestamp) AS inicio_intervalo,
        MAX(timestamp) AS fin_intervalo
    FROM Apuestas
    WHERE timestamp >= NOW() - INTERVAL '5 minutes'
    GROUP BY
        evento_id,
        monto_apostado,
        cuota,
        FLOOR(EXTRACT(EPOCH FROM timestamp) / 300) -- Agrupar por intervalos de 5 minutos
)
SELECT *
FROM ApuestasAgrupadas
WHERE total_apuestas > 20;
