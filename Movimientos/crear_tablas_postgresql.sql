-- ============================================
-- CREAR TABLAS EN POSTGRESQL PARA RAILWAY
-- ============================================
-- Ejecutar esto en la consola de PostgreSQL en Railway
-- O subir este archivo y ejecutar: psql -f crear_tablas_postgresql.sql

-- Tabla de usuarios (auth_user) - Django la crea automáticamente
-- pero la incluyo por si acaso

-- Tabla Deuda
CREATE TABLE IF NOT EXISTS base_deuda (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    tipo VARCHAR(20) DEFAULT 'DEUDA',
    valor_inicial DECIMAL(15, 2) NOT NULL,
    valor_total_a_pagar DECIMAL(15, 2) NOT NULL,
    cuota_mensual DECIMAL(15, 2) NOT NULL,
    total_meses INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    descripcion TEXT,
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Transaccion
CREATE TABLE IF NOT EXISTS base_transaccion (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    deuda_id INTEGER,
    tipo VARCHAR(10) NOT NULL,
    categoria VARCHAR(100) DEFAULT 'General',
    monto DECIMAL(10, 2) NOT NULL,
    fecha DATE NOT NULL,
    descripcion TEXT
);

-- Tabla Perfil
CREATE TABLE IF NOT EXISTS base_perfil (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion VARCHAR(200),
    ciudad VARCHAR(100),
    pais VARCHAR(100) DEFAULT 'Colombia',
    fecha_nacimiento DATE,
    bio TEXT,
    avatar VARCHAR(10) DEFAULT '👤',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_transaccion_usuario ON base_transaccion(usuario_id);
CREATE INDEX IF NOT EXISTS idx_transaccion_deuda ON base_transaccion(deuda_id);
CREATE INDEX IF NOT EXISTS idx_deuda_usuario ON base_deuda(usuario_id);
CREATE INDEX IF NOT EXISTS idx_perfil_usuario ON base_perfil(usuario_id);

-- Verificar que las tablas se crearon
SELECT 'Tablas creadas exitosamente' as mensaje;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'base_%';
