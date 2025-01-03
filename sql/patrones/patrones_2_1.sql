-- Patrón 2.1: Detectar Usuarios con Más de 50 Apuestas en 10 Minutos

-- Nota: Este script requiere los siguientes índices que estan el el archivo crear_indices:
-- 1. `idx_apuestas_timestamp` para búsquedas basadas en tiempo.
-- 2. `idx_usuario_timestamp` para agrupaciones por usuario y tiempo.

-- Paso 2: Preprocesamiento inicial con agrupaciones fijas (opción rápida)
WITH BloquesFijos AS (
    SELECT 
        usuario_id, 
        COUNT(*) AS total_apuestas,
        MIN(timestamp) AS inicio_intervalo,
        MAX(timestamp) AS fin_intervalo
    FROM Apuestas
    GROUP BY usuario_id, 
             FLOOR(EXTRACT(EPOCH FROM timestamp) / 600) -- Agrupación por bloques de 10 minutos
    HAVING COUNT(*) > 50
)

-- Paso 3: Análisis detallado con ventanas deslizantes (opción precisa)
, ApuestasConVentanas AS (
    SELECT 
        usuario_id, 
        timestamp,
        COUNT(*) OVER (
            PARTITION BY usuario_id 
            ORDER BY timestamp 
            RANGE BETWEEN INTERVAL '10 minutes' PRECEDING AND CURRENT ROW
        ) AS apuestas_en_10_min
    FROM Apuestas
)

-- Paso 4: Combinar los resultados
SELECT 
    usuario_id,
    COUNT(*) AS total_apuestas_sospechosas,
    MIN(timestamp) AS inicio_intervalo,
    MAX(timestamp) AS fin_intervalo
FROM ApuestasConVentanas
WHERE apuestas_en_10_min > 50
GROUP BY usuario_id;