-- Crear tabla de Usuarios
CREATE TABLE Usuarios (
    id BIGSERIAL PRIMARY KEY, -- Clave primaria única, auto-incremental
    nombre VARCHAR(100) NOT NULL, -- Nombre del usuario, obligatorio
    correo VARCHAR(255) UNIQUE NOT NULL, -- Correo único, obligatorio
    saldo NUMERIC(12, 2) NOT NULL CHECK (saldo >= 0) -- Saldo, no puede ser negativo
);

-- Crear tabla de Eventos
CREATE TABLE Eventos (
    id BIGSERIAL PRIMARY KEY, -- Clave primaria única, auto-incremental
    tipo_deporte VARCHAR(50) NOT NULL, -- Tipo de deporte (Fútbol, Tenis, etc.)
    equipos_participantes JSONB NOT NULL, -- Detalles de los equipos o participantes
    fecha_hora TIMESTAMP NOT NULL -- Fecha y hora del evento
);

-- Crear tabla de Apuestas
CREATE TABLE Apuestas (
    id BIGSERIAL PRIMARY KEY, -- Clave primaria única, auto-incremental
    usuario_id BIGINT NOT NULL REFERENCES Usuarios (id), -- Clave foránea a Usuarios
    evento_id BIGINT NOT NULL REFERENCES Eventos (id), -- Clave foránea a Eventos
    monto_apostado NUMERIC(12, 2) NOT NULL CHECK (monto_apostado > 0), -- Monto, obligatorio
    cuota NUMERIC(5, 2) NOT NULL CHECK (cuota > 0), -- Cuota, obligatorio
    resultado VARCHAR(10) CHECK (resultado IN ('ganada', 'perdida')), -- Resultado permitido
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha y hora de la apuesta
);
