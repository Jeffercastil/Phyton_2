#!/usr/bin/env python3
"""
Script para migrar datos de SQL Server a PostgreSQL
Ejecutar localmente antes de hacer deploy en Railway
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Movimientos.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import pyodbc
import psycopg2
from django.contrib.auth.models import User
from aplicaciones.base.models import Transaccion, Deuda, Perfil
from decimal import Decimal
from datetime import datetime

def get_sql_server_connection():
    """Conectar a SQL Server local"""
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-7L879NC\\SQLEXPRESS;'
            'DATABASE=DJANGO_MOVIMIENTOS;'
            'UID=Jefrino;'
            'PWD=Emily2713*cas;'
            'PORT=1433;'
        )
        print("✅ Conectado a SQL Server")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a SQL Server: {e}")
        return None

def exportar_datos_sql_server():
    """Exportar datos de SQL Server a archivos JSON"""
    conn = get_sql_server_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    datos = {
        'usuarios': [],
        'transacciones': [],
        'deudas': [],
        'perfiles': []
    }

    try:
        # Exportar usuarios
        print("\n📤 Exportando usuarios...")
        cursor.execute("SELECT id, username, email, first_name, last_name, date_joined, is_active FROM auth_user")
        for row in cursor.fetchall():
            datos['usuarios'].append({
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'first_name': row[3],
                'last_name': row[4],
                'date_joined': row[5],
                'is_active': row[6]
            })
        print(f"   ✅ {len(datos['usuarios'])} usuarios exportados")

        # Exportar transacciones
        print("\n📤 Exportando transacciones...")
        cursor.execute("""
            SELECT id, usuario_id, deuda_id, tipo, categoria, monto, fecha, descripcion
            FROM base_transaccion
        """)
        for row in cursor.fetchall():
            datos['transacciones'].append({
                'id': row[0],
                'usuario_id': row[1],
                'deuda_id': row[2],
                'tipo': row[3],
                'categoria': row[4],
                'monto': float(row[5]) if row[5] else 0,
                'fecha': row[6].strftime('%Y-%m-%d') if row[6] else None,
                'descripcion': row[7]
            })
        print(f"   ✅ {len(datos['transacciones'])} transacciones exportadas")

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
                    'descripcion': row[9],
                    'activa': row[10],
                    'fecha_creacion': row[11].isoformat() if row[11] else None
                })
            print(f"   ✅ {len(datos['deudas'])} deudas exportadas")
        except Exception as e:
            print(f"   ⚠️  No se pudieron exportar deudas: {e}")

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
                    'telefono': row[2],
                    'direccion': row[3],
                    'ciudad': row[4],
                    'pais': row[5],
                    'fecha_nacimiento': row[6].strftime('%Y-%m-%d') if row[6] else None,
                    'bio': row[7],
                    'avatar': row[8],
                    'fecha_registro': row[9].isoformat() if row[9] else None
                })
            print(f"   ✅ {len(datos['perfiles'])} perfiles exportados")
        except Exception as e:
            print(f"   ⚠️  No se pudieron exportar perfiles: {e}")

        conn.close()

        # Guardar a JSON
        import json
        with open('datos_exportados.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        print("\n" + "="*50)
        print("✅ DATOS EXPORTADOS CORRECTAMENTE")
        print("="*50)
        print(f"Archivo: datos_exportados.json")
        print(f"Ubicación: {os.path.abspath('datos_exportados.json')}")
        print("\nAhora sube este archivo a Railway y ejecuta:")
        print("python importar_a_postgresql.py")
        return True

    except Exception as e:
        print(f"❌ Error exportando datos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("="*50)
    print("EXPORTADOR SQL SERVER → JSON")
    print("="*50)
    exportar_datos_sql_server()
