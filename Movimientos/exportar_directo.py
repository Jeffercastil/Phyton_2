#!/usr/bin/env python3
"""
Exportar datos usando pyodbc directamente (sin Django)
"""

import pyodbc
import json
import os

print("="*60)
print("EXPORTADOR DIRECTO SQL SERVER → JSON")
print("="*60)
print()

# Configuración de conexión
SERVER = 'DESKTOP-7L879NC\\SQLEXPRESS'
DATABASE = 'DJANGO_MOVIMIENTOS'
USERNAME = 'Jefrino'
PASSWORD = 'Emily2713*cas'

print(f"Conectando a SQL Server...")
print(f"  Servidor: {SERVER}")
print(f"  Base de datos: {DATABASE}")
print(f"  Usuario: {USERNAME}")
print()

try:
    # Intentar conectar con diferentes drivers
    drivers = [
        'ODBC Driver 17 for SQL Server',
        'ODBC Driver 18 for SQL Server',
        'SQL Server Native Client 11.0',
        'SQL Server'
    ]

    conn = None
    for driver in drivers:
        try:
            print(f"Probando driver: {driver}")
            conn_str = (
                f'DRIVER={{{driver}}};'
                f'SERVER={SERVER};'
                f'DATABASE={DATABASE};'
                f'UID={USERNAME};'
                f'PWD={PASSWORD};'
                f'Timeout=10;'
            )
            conn = pyodbc.connect(conn_str)
            print(f"✅ Conectado con driver: {driver}")
            break
        except Exception as e:
            print(f"  ❌ Falló: {e}")
            continue

    if not conn:
        print("❌ No se pudo conectar con ningún driver")
        print("\nDrivers disponibles:")
        for driver in pyodbc.drivers():
            print(f"  - {driver}")
        input("\nPresiona Enter para salir...")
        exit(1)

    cursor = conn.cursor()

    datos = {
        'usuarios': [],
        'transacciones': [],
        'deudas': [],
        'perfiles': []
    }

    # Exportar usuarios
    print("\n📤 Exportando usuarios...")
    try:
        cursor.execute("SELECT id, username, email, first_name, last_name, date_joined, is_active FROM auth_user")
        for row in cursor.fetchall():
            datos['usuarios'].append({
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'first_name': row[3] or '',
                'last_name': row[4] or '',
                'date_joined': row[5].isoformat() if row[5] else None,
                'is_active': row[6]
            })
        print(f"   ✅ {len(datos['usuarios'])} usuarios exportados")
    except Exception as e:
        print(f"   ⚠️ Error o tabla vacía: {e}")

    # Exportar transacciones
    print("\n📤 Exportando transacciones...")
    try:
        cursor.execute("SELECT id, usuario_id, deuda_id, tipo, categoria, monto, fecha, descripcion FROM base_transaccion")
        for row in cursor.fetchall():
            datos['transacciones'].append({
                'id': row[0],
                'usuario_id': row[1],
                'deuda_id': row[2],
                'tipo': row[3],
                'categoria': row[4],
                'monto': float(row[5]) if row[5] else 0,
                'fecha': row[6].strftime('%Y-%m-%d') if row[6] else None,
                'descripcion': row[7] or ''
            })
        print(f"   ✅ {len(datos['transacciones'])} transacciones exportadas")
    except Exception as e:
        print(f"   ⚠️ Error o tabla vacía: {e}")

    # Exportar deudas
    print("\n📤 Exportando deudas...")
    try:
        cursor.execute("""
            SELECT id, usuario_id, nombre, tipo, valor_inicial, valor_total_a_pagar,
                   cuota_mensual, total_meses, fecha_inicio, descripcion, activa, fecha_creacion
            FROM base_deuda
        """)
        for row in cursor.fetchall():
            datos['deudas'].append({
                'id': row[0],
                'usuario_id': row[1],
                'nombre': row[2],
                'tipo': row[3],
                'valor_inicial': float(row[4]) if row[4] else 0,
                'valor_total_a_pagar': float(row[5]) if row[5] else 0,
                'cuota_mensual': float(row[6]) if row[6] else 0,
                'total_meses': row[7],
                'fecha_inicio': row[8].strftime('%Y-%m-%d') if row[8] else None,
                'descripcion': row[9] or '',
                'activa': row[10],
                'fecha_creacion': row[11].isoformat() if row[11] else None
            })
        print(f"   ✅ {len(datos['deudas'])} deudas exportadas")
    except Exception as e:
        print(f"   ⚠️ Error o tabla vacía: {e}")

    # Exportar perfiles
    print("\n📤 Exportando perfiles...")
    try:
        cursor.execute("""
            SELECT id, usuario_id, telefono, direccion, ciudad, pais,
                   fecha_nacimiento, bio, avatar, fecha_registro
            FROM base_perfil
        """)
        for row in cursor.fetchall():
            datos['perfiles'].append({
                'id': row[0],
                'usuario_id': row[1],
                'telefono': row[2] or '',
                'direccion': row[3] or '',
                'ciudad': row[4] or '',
                'pais': row[5] or 'Colombia',
                'fecha_nacimiento': row[6].strftime('%Y-%m-%d') if row[6] else None,
                'bio': row[7] or '',
                'avatar': row[8] or '👤',
                'fecha_registro': row[9].isoformat() if row[9] else None
            })
        print(f"   ✅ {len(datos['perfiles'])} perfiles exportados")
    except Exception as e:
        print(f"   ⚠️ Error o tabla vacía: {e}")

    conn.close()

    # Guardar a JSON
    with open('datos_exportados.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

    print("\n" + "="*60)
    print("✅ EXPORTACIÓN COMPLETADA")
    print("="*60)
    print()
    print(f"📁 Archivo creado: datos_exportados.json")
    print(f"📍 Ubicación: {os.path.abspath('datos_exportados.json')}")
    print()
    print("📊 Resumen de datos exportados:")
    print(f"   • Usuarios: {len(datos['usuarios'])}")
    print(f"   • Transacciones: {len(datos['transacciones'])}")
    print(f"   • Deudas: {len(datos['deudas'])}")
    print(f"   • Perfiles: {len(datos['perfiles'])}")
    print()
    print("🚀 Siguiente paso: Subir a GitHub ejecutando:")
    print("   git add datos_exportados.json")
    print("   git commit -m 'Datos exportados'")
    print("   git push")
    print()
    print("Luego ve a Railway y crea PostgreSQL (New → Database → Add PostgreSQL)")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print()
input("Presiona Enter para cerrar...")
