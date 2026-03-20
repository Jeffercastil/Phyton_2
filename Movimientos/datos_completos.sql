-- ============================================
-- CREAR TABLAS E IMPORTAR DATOS EN POSTGRESQL
-- Ejecutar esto en Railway PostgreSQL
-- ============================================

-- Crear tablas
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

-- Insertar transacciones
INSERT INTO base_transaccion (id, usuario_id, deuda_id, tipo, categoria, monto, fecha, descripcion) VALUES
(1202, 1, NULL, 'GASTO', 'gasto-varios', 20000.00, '2025-05-30', 'Pago de gasolina'),
(1203, 1, NULL, 'GASTO', 'gasto-varios', 35000.00, '2025-06-01', 'Parrillada, por valor de 35 que se lo debo pagar a lesly'),
(1204, 1, NULL, 'GASTO', 'obligacion', 350000.00, '2025-05-30', 'Pago parcial del arriendo por un valor de 350 y en total son 500, faltaria el segundo pago de 150'),
(1205, 1, NULL, 'GASTO', 'gasto-varios', 47500.00, '2025-06-06', 'Pago que le debo a mayerly El pedido Son  30400 +17100'),
(1206, 1, NULL, 'GASTO', 'gasto-varios', 300000.00, '2025-06-15', 'Me prestaron 300 mil para el tema del trasteo y parte del arriendo de la habitacion, todavia debo esto y espero pagarlo el 15 de junio'),
(1207, 1, NULL, 'INGRESO', 'pago-nomina', 2133075.00, '2025-01-30', 'pago del mes de enero del 16 al 31'),
(1208, 1, NULL, 'INGRESO', 'pago-nomina', 1564021.00, '2025-02-14', 'Pago del 1 al 15 de febrero'),
(1209, 1, NULL, 'INGRESO', 'pago-nomina', 1736434.00, '2025-02-28', 'Pago del 15 al 28 de febrero'),
(1210, 1, NULL, 'INGRESO', 'pago-nomina', 1303732.00, '2025-03-14', 'pago del 1 al 15 de marzo'),
(1211, 1, NULL, 'INGRESO', 'pago-nomina', 1748228.00, '2025-03-28', 'pago del 16 al 31 de marzo'),
(1212, 1, NULL, 'INGRESO', 'pago-nomina', 1617940.00, '2025-04-15', 'pago del mes de abril del 1 al 15'),
(1213, 1, NULL, 'INGRESO', 'pago-nomina', 1572229.00, '2025-04-30', 'pago del mes de abril del 16 al 30'),
(1214, 1, NULL, 'GASTO', 'deuda-prestamo', 250000.00, '2025-05-15', 'pago del prestamo'),
(1215, 1, NULL, 'INGRESO', 'pago-nomina', 1656224.00, '2025-05-15', 'pago del mes de mayo del 1 al 15'),
(1216, 1, NULL, 'GASTO', 'ahorro-inversion', 100000.00, '2025-05-16', 'dinero invertido por lesly'),
(1217, 1, NULL, 'INGRESO', 'pago-nomina', 1676024.00, '2025-05-30', 'pago del mes de mayo del 16 al 31'),
(1218, 1, NULL, 'GASTO', 'deuda-prestamo', 250000.00, '2025-06-14', 'pago de la deuda'),
(1219, 1, NULL, 'INGRESO', 'pago-nomina', 1761223.00, '2025-06-15', 'pago del mes de junio del 1 al 15');

-- Verificar datos insertados
SELECT 'Tablas creadas y datos importados' as mensaje;
SELECT COUNT(*) as total_transacciones FROM base_transaccion;
