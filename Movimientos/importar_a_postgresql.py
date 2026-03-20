#!/usr/bin/env python3
"""
Script para importar datos a PostgreSQL en Railway
Subir este archivo junto con datos_exportados.json a Railway
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Movimientos.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import json
from django.contrib.auth.models import User
from aplicaciones.base.models import Transaccion, Deuda, Perfil
from decimal import Decimal
from datetime import datetime

def importar_datos():
    """Importar datos desde JSON a PostgreSQL"""

    if not os.path.exists('datos_exportados.json'):
        print("❌ No se encontró el archivo datos_exportados.json")
        print("Primero ejecuta en tu computadora: python exportar_sql_server.py")
        return False

    with open('datos_exportados.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)

    print("="*50)
    print("IMPORTANDO DATOS A POSTGRESQL")
    print("="*50)

    # Mapeo de IDs antiguos a nuevos
    user_id_map = {}
    deuda_id_map = {}

    # 1. Importar usuarios
    print("\n📥 Importando usuarios...")
    for user_data in datos['usuarios']:
        try:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'] or '',
                    'last_name': user_data['last_name'] or '',
                }
            )
            if created:
                user.set_password('temporal123')  # Contraseña temporal
                user.save()
                print(f"   ✅ Creado usuario: {user.username}")
            else:
                print(f"   ℹ️  Usuario ya existe: {user.username}")
            user_id_map[user_data['id']] = user.id
        except Exception as e:
            print(f"   ❌ Error con usuario {user_data['username']}: {e}")

    print(f"\n   Total usuarios mapeados: {len(user_id_map)}")

    # 2. Importar deudas
    print("\n📥 Importando deudas...")
    for deuda_data in datos['deudas']:
        try:
            if deuda_data['usuario_id'] not in user_id_map:
                print(f"   ⚠️  Usuario no encontrado para deuda: {deuda_data['nombre']}")
                continue

            nueva_deuda = Deuda.objects.create(
                usuario_id=user_id_map[deuda_data['usuario_id']],
                nombre=deuda_data['nombre'],
                tipo=deuda_data['tipo'],
                valor_inicial=Decimal(str(deuda_data['valor_inicial'])),
                valor_total_a_pagar=Decimal(str(deuda_data['valor_total_a_pagar'])),
                cuota_mensual=Decimal(str(deuda_data['cuota_mensual'])),
                total_meses=deuda_data['total_meses'],
                fecha_inicio=deuda_data['fecha_inicio'] or datetime.now().date(),
                descripcion=deuda_data['descripcion'] or '',
                activa=deuda_data['activa']
            )
            deuda_id_map[deuda_data['id']] = nueva_deuda.id
            print(f"   ✅ Deuda creada: {nueva_deuda.nombre}")
        except Exception as e:
            print(f"   ❌ Error creando deuda {deuda_data.get('nombre', 'N/A')}: {e}")

    print(f"\n   Total deudas mapeadas: {len(deuda_id_map)}")

    # 3. Importar transacciones
    print("\n📥 Importando transacciones...")
    count = 0
    for trans_data in datos['transacciones']:
        try:
            if trans_data['usuario_id'] not in user_id_map:
                print(f"   ⚠️  Usuario no encontrado para transacción")
                continue

            deuda = None
            if trans_data['deuda_id'] and trans_data['deuda_id'] in deuda_id_map:
                deuda_id = deuda_id_map[trans_data['deuda_id']]
                try:
                    deuda = Deuda.objects.get(id=deuda_id)
                except Deuda.DoesNotExist:
                    pass

            Transaccion.objects.create(
                usuario_id=user_id_map[trans_data['usuario_id']],
                deuda=deuda,
                tipo=trans_data['tipo'],
                categoria=trans_data['categoria'],
                monto=Decimal(str(trans_data['monto'])),
                fecha=trans_data['fecha'] or datetime.now().date(),
                descripcion=trans_data['descripcion'] or ''
            )
            count += 1
            if count % 10 == 0:
                print(f"   ... {count} transacciones importadas")
        except Exception as e:
            print(f"   ❌ Error creando transacción: {e}")

    print(f"\n   ✅ Total transacciones importadas: {count}")

    # 4. Importar perfiles
    print("\n📥 Importando perfiles...")
    for perfil_data in datos['perfiles']:
        try:
            if perfil_data['usuario_id'] not in user_id_map:
                print(f"   ⚠️  Usuario no encontrado para perfil")
                continue

            Perfil.objects.get_or_create(
                usuario_id=user_id_map[perfil_data['usuario_id']],
                defaults={
                    'telefono': perfil_data.get('telefono', ''),
                    'direccion': perfil_data.get('direccion', ''),
                    'ciudad': perfil_data.get('ciudad', ''),
                    'pais': perfil_data.get('pais', 'Colombia'),
                    'bio': perfil_data.get('bio', ''),
                    'avatar': perfil_data.get('avatar', '👤'),
                }
            )
            print(f"   ✅ Perfil creado para usuario ID {perfil_data['usuario_id']}")
        except Exception as e:
            print(f"   ❌ Error creando perfil: {e}")

    print("\n" + "="*50)
    print("✅ IMPORTACIÓN COMPLETADA")
    print("="*50)
    print("\nResumen:")
    print(f"  - Usuarios: {len(user_id_map)}")
    print(f"  - Deudas: {len(deuda_id_map)}")
    print(f"  - Transacciones: {count}")
    print("\n⚠️  IMPORTANTE: Cambia las contraseñas de los usuarios")
    print("   La contraseña temporal es: 'temporal123'")

    return True

if __name__ == '__main__':
    importar_datos()
