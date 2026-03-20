-- ============================================
-- SCRIPT PARA EXPORTAR DATOS DE SQL SERVER
-- ============================================
-- Ejecuta esto en SQL Server Management Studio
-- Luego guarda los resultados como CSV

-- 1. Ver tabla de transacciones
SELECT * FROM base_transaccion;

-- 2. Ver tabla de deudas (si existe)
SELECT * FROM base_deuda;

-- 3. Ver tabla de perfiles (si existe)
SELECT * FROM base_perfil;

-- 4. Ver usuarios
SELECT * FROM auth_user;
