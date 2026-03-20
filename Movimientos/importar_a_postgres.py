#!/usr/bin/env python3
"""
Importar datos a PostgreSQL en Railway
Este script se ejecuta en Railway
"""

import os
import sys
import json

print("="*60)
print("IMPORTANDO DATOS A POSTGRESQL")
print("="*60)
print()

# Verificar si existe el archivo de datos
if not os.path.exists('datos_exportados.json'):
    print("⚠️  No se encontró datos_exportados.json")
    print("Continuando sin importar datos...")
    sys.exit(0)

# Cargar datos
with open('datos_exportados.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

print(f"📁 Datos cargados:")
print(f"   - Usuarios: {len(datos.get('usuarios', []))}")
print(f"   - Transacciones: {len(datos.get('transacciones', []))}")
print(f"   - Deudas: {len(datos.get('deudas', []))}")
print(f"   - Perfiles: {len(datos.get('perfiles', []))}")
print()

# Intentar importar a PostgreSQL
try:
    import psycopg2
    from urllib.parse import urlparse

    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("⚠️  DATABASE_URL no configurada")
        sys.exit(0)

    result = urlparse(database_url)
    conn = psycopg2.connect(
        host=result.hostname,
        port=result.port,
        database=result.path[1:],
        user=result.username,
        password=result.password
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print("✅ Conectado a PostgreSQL")
    print()

    # Crear tablas
    print("📦 Creando tablas...")
    cursor.execute("""
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
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS base_transaccion (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL,
            deuda_id INTEGER,
            tipo VARCHAR(10) NOT NULL,
            categoria VARCHAR(100) DEFAULT 'General',
            monto DECIMAL(10, 2) NOT NULL,
            fecha DATE NOT NULL,
            descripcion TEXT
        )
    """)

    cursor.execute("""
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
        )
    """)
    print("✅ Tablas creadas")
    print()

    # Importar datos
    if datos.get('deudas'):
        print("📥 Importando deudas...")
        for deuda in datos['deudas']:
            try:
                cursor.execute("""
                    INSERT INTO base_deuda
                    (id, usuario_id, nombre, tipo, valor_inicial, valor_total_a_pagar,
                     cuota_mensual, total_meses, fecha_inicio, descripcion, activa, fecha_creacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    deuda['id'], deuda['usuario_id'], deuda['nombre'], deuda['tipo'],
                    deuda['valor_inicial'], deuda['valor_total_a_pagar'], deuda['cuota_mensual'],
                    deuda['total_meses'], deuda['fecha_inicio'], deuda['descripcion'],
                    deuda['activa'], deuda['fecha_creacion']
                ))
            except Exception as e:
                pass
        print("   ✅ Deudas importadas")
        print()

    if datos.get('transacciones'):
        print("📥 Importando transacciones...")
        for trans in datos['transacciones']:
            try:
                cursor.execute("""
                    INSERT INTO base_transaccion
                    (id, usuario_id, deuda_id, tipo, categoria, monto, fecha, descripcion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    trans['id'], trans['usuario_id'], trans['deuda_id'], trans['tipo'],
                    trans['categoria'], trans['monto'], trans['fecha'], trans['descripcion']
                ))
            except Exception as e:
                pass
        print("   ✅ Transacciones importadas")
        print()

    if datos.get('perfiles'):
        print("📥 Importando perfiles...")
        for perfil in datos['perfiles']:
            try:
                cursor.execute("""
                    INSERT INTO base_perfil
                    (id, usuario_id, telefono, direccion, ciudad, pais, fecha_nacimiento, bio, avatar, fecha_registro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    perfil['id'], perfil['usuario_id'], perfil.get('telefono'),
                    perfil.get('direccion'), perfil.get('ciudad'), perfil.get('pais'),
                    perfil.get('fecha_nacimiento'), perfil.get('bio'),
                    perfil.get('avatar', '👤'), perfil.get('fecha_registro')
                ))
            except Exception as e:
                pass
        print("   ✅ Perfiles importados")
        print()

    conn.close()
    print("="*60)
    print("✅ IMPORTACIÓN COMPLETADA")
    print("="*60)

except ImportError as e:
    print(f"⚠️  No se pudo importar psycopg2: {e}")
    print("Las tablas se crearán con las migraciones de Django")
except Exception as e:
    print(f"⚠️  Error durante la importación: {e}")
    print("Continuando con el inicio de la aplicación...")

print()
