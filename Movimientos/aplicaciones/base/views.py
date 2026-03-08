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
from .models import Cliente, Transaccion

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
# --- VISTA DE LISTA DE CLIENTES ---
@login_required
def clientes_lista(request):
    # Busca en la tabla Cliente todos los registros donde el 'propietario' sea el usuario logueado.
    clientes = Cliente.objects.filter(propietario=request.user)
    
    # Renderiza el HTML y le pasa la lista de clientes encontrados.
    return render(request, 'base/clientes.html', {'clientes': clientes})


# --- VISTA DE LISTA DE TRANSACCIONES ---
@login_required
def transacciones_lista(request):
    # Leer filtros del GET
    anio = request.GET.get('anio', '')
    mes  = request.GET.get('mes', '')
    tipo = request.GET.get('tipo', '')
    categoria = request.GET.get('categoria', '')

    # Queryset base
    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')

    # Aplicar filtros si existen
    if anio:
        transacciones = transacciones.filter(fecha__year=anio)
    if mes:
        transacciones = transacciones.filter(fecha__month=mes)
    if tipo:
        transacciones = transacciones.filter(tipo=tipo)
    if categoria:
        transacciones = transacciones.filter(categoria__icontains=categoria)

    # Clientes para el selector del modal
    clientes = Cliente.objects.filter(propietario=request.user)

    # Categorías únicas del usuario para el select de filtro
    categorias_disponibles = Transaccion.objects.filter(
        usuario=request.user
    ).values_list('categoria', flat=True).distinct().order_by('categoria')

    context = {
        'transacciones': transacciones,
        'clientes': clientes,
        'categorias_disponibles': categorias_disponibles,
    }
    return render(request, 'base/transacciones.html', context)



# --- API PARA CREAR CLIENTE (Backend para JavaScript) ---
@login_required # Debes estar logueado.
@csrf_exempt    # Eximimos de la protección CSRF para que peticiones externas (JS) funcionen fácilmente.
def crear_cliente(request):
    # Verificamos si el método de la petición es POST (cuando se envían datos para guardar).
    if request.method == 'POST':
        
        # request.body contiene los datos crudos enviados por el frontend (texto).
        # json.loads convierte ese texto en un diccionario de Python usable.
        data = json.loads(request.body)
        
        # Crea un nuevo registro en la base de datos en la tabla Cliente.
        # Los datos (data['nombre'], etc.) vienen del JavaScript.
        cliente = Cliente.objects.create(
            documento_identidad=data['documento_identidad'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono'],
            correo=data['correo'],
            propietario=request.user # Asigna el cliente al usuario que está logueado ahora.
        )
        
        # Devuelve una respuesta al JavaScript en formato JSON confirmando el éxito.
        return JsonResponse({
            'success': True,
            'id': cliente.id,
            'nombre': cliente.nombre
        })
    
    # Si alguien intenta entrar a esta URL por el navegador (GET), devuelve error falso.
    return JsonResponse({'success': False})


# --- API PARA CREAR TRANSACCIÓN ---
@login_required
@csrf_exempt
def crear_transaccion(request):
    if request.method == 'POST':
        # Convertimos los datos enviados a Python.
        data = json.loads(request.body)
        
        # Inicializamos cliente como vacío (None).
        cliente = None

        # Obtener fecha del JSON o usar hoy
        fecha_str = data.get('fecha')
        if fecha_str:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        else:
            from django.utils import timezone
            fecha = timezone.now().date()        

        
        # Si en los datos enviados viene un 'cliente_id' (es opcional):
        if data.get('cliente_id'):
            # Busca ese cliente en la base de datos para asignarlo a la transacción.
            cliente = Cliente.objects.get(id=data['cliente_id'])
        
        # Crea la transacción en la base de datos.
        # Decimal(...) convierte el texto del monto a un tipo numérico preciso para dinero.
        transaccion = Transaccion.objects.create(
            usuario=request.user,
            cliente=cliente, # Puede ser None o un objeto Cliente.
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