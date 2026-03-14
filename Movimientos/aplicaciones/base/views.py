# --- IMPORTACIONES: Traemos las herramientas que necesitamos ---
# 'render': Sirve para cargar un archivo HTML y mostrarlo al usuario.
# 'redirect': Sirve para enviar al usuario a otra página.
# 'get_object_or_404': Busca algo en la base de datos, y si no existe, da error 404.
from django.shortcuts import render, redirect, get_object_or_404

# 'login_required': Es un guardia. Si no estás logueado, te manda al login automáticamente.
from django.contrib.auth.decorators import login_required
# Importa el sistema de mensajes de Django para mostrar notificaciones al usuario
from django.contrib import messages
# 'JsonResponse': Para devolver datos en formato JSON (útil para APIs y JavaScript).
from django.http import JsonResponse
# Importa pandas para leer y manipular archivos Excel
import pandas as pd
# Importa Decimal para manejar operaciones monetarias con precisión decimal
from decimal import Decimal
# 'csrf_exempt': Desactiva una protección de seguridad de Django. 
# (Nota: Se usa aquí para simplificar llamadas desde JS, pero en producción se maneja de otra forma).
from django.views.decorators.csrf import csrf_exempt

# 'models': Nos ayuda a hacer cálculos en la base de datos (como sumas).
from django.db import models

# Importa datetime para trabajar con fechas
from datetime import datetime

# Importamos nuestras tablas (Modelos) definidas en models.py de esta app.
from .models import Transaccion, Deuda, Perfil

# Importamos el modelo de Usuario de Django.
from django.contrib.auth.models import User

# 'json': Para poder leer datos que nos envían en formato texto (crudo) y convertirlos a Python.
import json

# 'Decimal': Para manejar dinero con precisión matemática (evita errores de los números flotantes).
from decimal import Decimal
from django.db.models import Sum

# --- VISTA PRINCIPAL: DASHBOARD ---
# El símbolo '@' es un "decorador". Modifica la función de abajo.
# Aquí dice: "Solo ejecuta esta función si el usuario ha iniciado sesión".

@login_required  # ← Este decorador es OBLIGATORIO, faltaba en la segunda versión
def dashboard(request):
    # Leer filtros del GET
    anio = request.GET.get('anio', '')
    mes = request.GET.get('mes', '')
    
    # Queryset base — SOLO del usuario logueado
    transacciones = Transaccion.objects.filter(usuario=request.user)
    
    # Aplicar filtros si existen
    if anio:
        transacciones = transacciones.filter(fecha__year=anio)
    if mes:
        transacciones = transacciones.filter(fecha__month=mes)
    
    # Calcular totales CON los filtros aplicados
    total_ingresos = transacciones.filter(tipo='INGRESO').aggregate(
        total=Sum('monto'))['total'] or 0
    total_gastos = transacciones.filter(tipo='GASTO').aggregate(
        total=Sum('monto'))['total'] or 0
    balance = total_ingresos - total_gastos
    
    # Últimas transacciones filtradas
    ultimas_transacciones = transacciones.order_by('-fecha')[:10]
    
    # Datos para gráfica
    categorias_data = transacciones.filter(tipo='GASTO').values(
        'categoria').annotate(total=Sum('monto')).order_by('-total')
    
    categorias_json = json.dumps([c['categoria'] for c in categorias_data])
    valores_json = json.dumps([float(c['total']) for c in categorias_data])
    
    return render(request, 'base/dashboard.html', {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': balance,
        'ultimas_transacciones': ultimas_transacciones,
        'categorias_json': categorias_json,
        'valores_json': valores_json,
    })


# --- VISTA DE LISTA DE TRANSACCIONES ---
@login_required
def transacciones_lista(request):
    anio = request.GET.get('anio', '')
    mes  = request.GET.get('mes', '')
    tipo = request.GET.get('tipo', '')
    categoria = request.GET.get('categoria', '')

    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')

    if anio:
        transacciones = transacciones.filter(fecha__year=anio)
    if mes:
        transacciones = transacciones.filter(fecha__month=mes)
    if tipo:
        transacciones = transacciones.filter(tipo=tipo)
    if categoria:
        transacciones = transacciones.filter(categoria__icontains=categoria)

    categorias_disponibles = Transaccion.objects.filter(
        usuario=request.user
    ).values_list('categoria', flat=True).distinct().order_by('categoria')

    # --- DATOS PARA GRÁFICAS ---
    base_qs = Transaccion.objects.filter(usuario=request.user)
    if anio:
        base_qs = base_qs.filter(fecha__year=anio)
    if mes:
        base_qs = base_qs.filter(fecha__month=mes)

    total_ingresos = base_qs.filter(tipo='INGRESO').aggregate(t=Sum('monto'))['t'] or 0
    total_gastos   = base_qs.filter(tipo='GASTO').aggregate(t=Sum('monto'))['t'] or 0

    top_gastos = base_qs.filter(tipo='GASTO').values('categoria').annotate(
        total=Sum('monto')).order_by('-total')[:8]

    context = {
        'transacciones': transacciones,
        'categorias_disponibles': categorias_disponibles,
        'total_ingresos': float(total_ingresos),
        'total_gastos': float(total_gastos),
        'top_categorias_json': json.dumps([x['categoria'] for x in top_gastos]),
        'top_valores_json':    json.dumps([float(x['total']) for x in top_gastos]),
    }
    return render(request, 'base/transacciones.html', context)



@login_required
def deudas_lista(request):
    deudas = Deuda.objects.filter(usuario=request.user, activa=True).order_by('-fecha_creacion')
    
    # Datos para gráficas del dashboard
    total_deuda = sum(float(d.saldo_pendiente()) for d in deudas)
    total_pagado = sum(float(d.total_pagado()) for d in deudas)
    
    # Preparar datos de cada deuda para el template
    deudas_data = []
    for d in deudas:
        deudas_data.append({
            'deuda': d,
            'total_pagado': float(d.total_pagado()),
            'saldo_pendiente': float(d.saldo_pendiente()),
            'meses_pagados': d.meses_pagados(),
            'meses_restantes': d.meses_restantes(),
            'porcentaje_pagado': d.porcentaje_pagado(),
            'interes_pagado': d.interes_pagado(),
            'interes_total': float(d.interes_total()),
        })
    
    # JSON para gráficas
    nombres_json = json.dumps([d['deuda'].nombre for d in deudas_data])
    pendientes_json = json.dumps([d['saldo_pendiente'] for d in deudas_data])
    pagados_json = json.dumps([d['total_pagado'] for d in deudas_data])

    return render(request, 'base/deudas.html', {
        'deudas_data': deudas_data,
        'total_deuda': total_deuda,
        'total_pagado': total_pagado,
        'nombres_json': nombres_json,
        'pendientes_json': pendientes_json,
        'pagados_json': pagados_json,
    })


@login_required
@csrf_exempt
def crear_deuda(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            deuda = Deuda.objects.create(
                usuario=request.user,
                nombre=data['nombre'],
                tipo=data['tipo'],
                valor_inicial=Decimal(str(data['valor_inicial'])),
                valor_total_a_pagar=Decimal(str(data['valor_total_a_pagar'])),
                cuota_mensual=Decimal(str(data['cuota_mensual'])),
                total_meses=int(data['total_meses']),
                fecha_inicio=data['fecha_inicio'],
                descripcion=data.get('descripcion', '')
            )
            return JsonResponse({'success': True, 'id': deuda.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


@login_required
@csrf_exempt
def pagar_deuda(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            deuda = Deuda.objects.get(id=id, usuario=request.user)
            monto = Decimal(str(data['monto']))
            fecha_str = data.get('fecha')
            
            from django.utils import timezone
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else timezone.now().date()
            
            # Crear transacción de gasto asociada a la deuda
            Transaccion.objects.create(
                usuario=request.user,
                tipo='GASTO',
                categoria='deuda' if deuda.tipo == 'DEUDA' else 'deuda-reportado',
                monto=monto,
                fecha=fecha,
                descripcion=f'Pago deuda: {deuda.nombre}',
                deuda=deuda
            )
            
            # Si el saldo queda en 0, marcar como inactiva
            if deuda.saldo_pendiente() <= 0:
                deuda.activa = False
                deuda.save()
            
            return JsonResponse({
                'success': True,
                'saldo_pendiente': float(deuda.saldo_pendiente()),
                'porcentaje': deuda.porcentaje_pagado()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


@login_required
@csrf_exempt  
def eliminar_deuda(request, id):
    if request.method == 'POST':
        try:
            deuda = Deuda.objects.get(id=id, usuario=request.user)
            deuda.activa = False  # Soft delete
            deuda.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

# --- API PARA CREAR TRANSACCIÓN ---
@login_required
@csrf_exempt
def crear_transaccion(request):
    if request.method == 'POST':
        # Convertimos los datos enviados a Python.
        data = json.loads(request.body)

        # Obtener fecha del JSON o usar hoy
        fecha_str = data.get('fecha')
        if fecha_str:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        else:
            from django.utils import timezone
            fecha = timezone.now().date()

        # Crea la transacción en la base de datos.
        # Decimal(...) convierte el texto del monto a un tipo numérico preciso para dinero.
        transaccion = Transaccion.objects.create(
            usuario=request.user,
            tipo=data['tipo'],
            categoria=data['categoria'],
            monto=Decimal(data['monto']),
            # .get(..., '') intenta buscar descripcion, si no existe, pone un string vacío.
            descripcion=data.get('descripcion', ''),
            fecha=fecha,
        )

        # Responde al JavaScript que todo salió bien.
        return JsonResponse({
            'success': True,
            'id': transaccion.id
        })

    return JsonResponse({'success': False})


# --- VISTA PÚBLICA (HOME) ---
def index(request):
    # Esta función no tiene @login_required, así que cualquiera puede verla.
    # Simplemente muestra la página de inicio (Landing Page).
    return render(request, 'base/index.html')


@login_required
@csrf_exempt
def eliminar_transaccion(request, id):
    if request.method == 'POST':
        try:
            transaccion = Transaccion.objects.get(id=id, usuario=request.user)
            transaccion.delete()
            return JsonResponse({'success': True})
        except Transaccion.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Transacción no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


# ── AGREGAR en views.py, junto a las otras vistas de deuda ──

@login_required
@csrf_exempt
def editar_deuda(request, id):
    """Editar los datos de una deuda existente"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            deuda = Deuda.objects.get(id=id, usuario=request.user)

            deuda.nombre              = data.get('nombre', deuda.nombre)
            deuda.tipo                = data.get('tipo', deuda.tipo)
            deuda.valor_inicial       = Decimal(str(data.get('valor_inicial', deuda.valor_inicial)))
            deuda.valor_total_a_pagar = Decimal(str(data.get('valor_total_a_pagar', deuda.valor_total_a_pagar)))
            deuda.cuota_mensual       = Decimal(str(data.get('cuota_mensual', deuda.cuota_mensual)))
            deuda.total_meses         = int(data.get('total_meses', deuda.total_meses))
            deuda.fecha_inicio        = data.get('fecha_inicio', deuda.fecha_inicio)
            deuda.descripcion         = data.get('descripcion', deuda.descripcion)
            deuda.save()

            return JsonResponse({'success': True})
        except Deuda.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Deuda no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
@csrf_exempt
def obtener_transaccion(request, id):
    """Obtener datos de una transacción para ver/editar"""
    try:
        transaccion = Transaccion.objects.get(id=id, usuario=request.user)
        return JsonResponse({
            'success': True,
            'transaccion': {
                'id': transaccion.id,
                'fecha': transaccion.fecha.strftime('%d/%m/%Y'),
                'tipo': transaccion.tipo,
                'categoria': transaccion.categoria,
                'monto': float(transaccion.monto),
                'descripcion': transaccion.descripcion or '',
            }
        })
    except Transaccion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Transacción no encontrada'})


@login_required
@csrf_exempt
def editar_transaccion(request, id):
    """Editar una transacción existente"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            transaccion = Transaccion.objects.get(id=id, usuario=request.user)
            
            # Actualizar campos permitidos
            transaccion.categoria = data.get('categoria', transaccion.categoria)
            transaccion.monto = Decimal(data.get('monto', transaccion.monto))
            transaccion.descripcion = data.get('descripcion', transaccion.descripcion)
            transaccion.save()
            
            return JsonResponse({'success': True})
        except Transaccion.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Transacción no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required  # Decorador: solo usuarios logueados pueden acceder
def importar_excel(request):
    """
    Vista para importar transacciones desde un archivo Excel
    """
    # Solo procesamos si es POST (formulario enviado) y hay archivo subido
    if request.method == 'POST' and request.FILES.get('archivo_excel'):
        try:
            # Obtenemos el archivo del formulario
            archivo = request.FILES['archivo_excel']
            
            # Pandas lee el Excel y lo convierte en DataFrame (tabla)
            df = pd.read_excel(archivo, dtype = {'fecha': str})
            # Leer pestaña específica TRANSACCION de archivo .xlsb
           # df = pd.read_excel(archivo, sheet_name='TRANSACCION', engine='pyxlsb')
            
            # Definimos qué columnas debe tener el Excel
            columnas_requeridas = ['tipo', 'categoria', 'monto', 'descripcion', 'fecha']
            
            # Verificamos que el Excel tenga todas las columnas necesarias
            if not all(col in df.columns for col in columnas_requeridas):
                messages.error(request, f'El Excel debe tener estas columnas: {", ".join(columnas_requeridas)}')
                return redirect('base:transacciones')
            
            # Contadores para el resumen final
            creadas = 0      # Transacciones exitosas
            errores = []     # Lista de errores encontrados
            
            # iterrows() recorre el DataFrame fila por fila
            # index = número de fila (empieza en 0), row = datos de la fila
            for index, row in df.iterrows():
                try:
                    # Limpiamos el texto: mayúsculas y sin espacios
                    tipo = str(row['tipo']).upper().strip()
                    
                    # Validamos que el tipo sea correcto
                    if tipo not in ['INGRESO', 'GASTO']:
                        errores.append(f"Fila {index+2}: Tipo debe ser INGRESO o GASTO")
                        continue  # Saltamos a la siguiente fila
                    # Convertir fecha
                    fecha = pd.to_datetime(row['fecha'], errors='coerce').date()
                    if pd.isna(fecha):
                        fecha = datetime.now().date()
                    # Validar que la fecha no sea futura (opcional)
                    if fecha > datetime.now().date():
                        errores.append(f"Fila {index+2}: La fecha {fecha} es futura")
                        continue

                   
                    # Creamos el objeto en la base de datos
                    Transaccion.objects.create(
                        usuario=request.user,  # El usuario logueado
                        tipo=tipo,
                        categoria=str(row['categoria']),
                        monto=Decimal(str(row['monto'])),  # Decimal para precisión monetaria
                        fecha=fecha,
                        descripcion=str(row['descripcion']) if pd.notna(row['descripcion']) else ''
                    )
                    creadas += 1  # Sumamos al contador de éxitos
                    
                except Exception as e:
                    # Capturamos cualquier error de esta fila específica
                    errores.append(f"Fila {index+2}: {str(e)}")
            
            # Mostramos mensajes de resultado al usuario
            if creadas > 0:
                messages.success(request, f'✅ Se importaron {creadas} transacciones correctamente')
            if errores:
                for error in errores[:5]:  # Solo mostramos los primeros 5 errores
                    messages.warning(request, error)
            
            return redirect('base:transacciones')
            
        except Exception as e:
            # Error general (ej: archivo corrupto, no es Excel)
            messages.error(request, f'❌ Error al procesar el archivo: {str(e)}')
            return redirect('base:transacciones')
    
    # Si no es POST o no hay archivo, redirigimos
    return redirect('base:transacciones')


# ============================================
# VISTAS DE REGISTRO Y GESTIÓN DE USUARIOS
# ============================================

def registro(request):
    """
    Vista para registrar nuevos usuarios.
    Crea un usuario de Django y un perfil asociado.
    """
    # Si el usuario ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('base:dashboard')

    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        telefono = request.POST.get('telefono', '').strip()

        # Validaciones
        errores = []

        if not username:
            errores.append('El nombre de usuario es obligatorio.')
        elif len(username) < 3:
            errores.append('El nombre de usuario debe tener al menos 3 caracteres.')
        elif User.objects.filter(username=username).exists():
            errores.append('Este nombre de usuario ya está en uso.')

        if not email:
            errores.append('El correo electrónico es obligatorio.')
        elif User.objects.filter(email=email).exists():
            errores.append('Este correo electrónico ya está registrado.')

        if not password:
            errores.append('La contraseña es obligatoria.')
        elif len(password) < 6:
            errores.append('La contraseña debe tener al menos 6 caracteres.')

        if password != password_confirm:
            errores.append('Las contraseñas no coinciden.')

        # Si hay errores, mostrarlos
        if errores:
            for error in errores:
                messages.error(request, error)
            return render(request, 'base/registro.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'telefono': telefono,
            })

        # Crear el usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Crear el perfil asociado
            Perfil.objects.create(
                usuario=user,
                telefono=telefono
            )

            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
            return render(request, 'base/registro.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'telefono': telefono,
            })

    # GET: Mostrar formulario vacío
    return render(request, 'base/registro.html')


@login_required
def mi_perfil(request):
    """
    Vista para ver y editar el perfil del usuario logueado.
    """
    # Obtener o crear el perfil del usuario
    perfil, creado = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'avatar': '👤'}
    )

    if request.method == 'POST':
        # Actualizar datos del usuario
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()

        # Actualizar datos del perfil
        perfil.telefono = request.POST.get('telefono', '').strip()
        perfil.direccion = request.POST.get('direccion', '').strip()
        perfil.ciudad = request.POST.get('ciudad', '').strip()
        perfil.pais = request.POST.get('pais', '').strip()
        perfil.bio = request.POST.get('bio', '').strip()
        perfil.avatar = request.POST.get('avatar', '👤').strip()

        # Fecha de nacimiento
        fecha_nacimiento = request.POST.get('fecha_nacimiento', '').strip()
        if fecha_nacimiento:
            try:
                perfil.fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                pass

        perfil.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('base:mi_perfil')

    return render(request, 'base/perfil.html', {
        'perfil': perfil,
    })


@login_required
def cambiar_password(request):
    """
    Vista para cambiar la contraseña del usuario.
    """
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual', '')
        password_nueva = request.POST.get('password_nueva', '')
        password_confirmar = request.POST.get('password_confirmar', '')

        errores = []

        # Verificar contraseña actual
        if not request.user.check_password(password_actual):
            errores.append('La contraseña actual es incorrecta.')

        # Validar nueva contraseña
        if len(password_nueva) < 6:
            errores.append('La nueva contraseña debe tener al menos 6 caracteres.')

        if password_nueva != password_confirmar:
            errores.append('Las contraseñas no coinciden.')

        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            request.user.set_password(password_nueva)
            request.user.save()
            messages.success(request, 'Contraseña actualizada correctamente. Por favor, vuelve a iniciar sesión.')
            return redirect('login')

    return render(request, 'base/cambiar_password.html')