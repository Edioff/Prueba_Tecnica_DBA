-- Índices del Punto 1.3
-- Índice para búsquedas basadas en usuario y tiempo
CREATE INDEX usuario_apuestas_idx ON Apuestas (usuario_id, timestamp);

-- Índice para búsquedas basadas en eventos y tiempo
CREATE INDEX evento_apuestas_idx ON Apuestas (evento_id, timestamp);

-- ====================================
-- Índices del Punto 2.1
-- Índice para búsquedas basadas en tiempo
CREATE INDEX idx_apuestas_timestamp ON Apuestas (timestamp);

-- Índice compuesto para optimizar agrupaciones y ordenaciones por usuario y tiempo
CREATE INDEX idx_usuario_timestamp ON Apuestas (usuario_id, timestamp);

-- ====================================
-- Índices del Patrón 2.2
CREATE INDEX idx_apuestas_identicas ON Apuestas (evento_id, monto_apostado, cuota, timestamp);
