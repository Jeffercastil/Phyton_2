# --- IMPORTACIONES: Traemos las herramientas que necesitamos ---
# 'render': Sirve para cargar un archivo HTML y mostrarlo al usuario.
# 'redirect': Sirve para enviar al usuario a otra página.
# 'get_object_or_404': Busca algo en la base de datos, y si no existe, da error 404.
from django.shortcuts import render, redirect, get_object_or_404

# 'login_required': Es un guardia. Si no estás logueado, te manda al login automáticamente.
from django.contrib.auth.decorators import login_required

# 'JsonResponse': Para devolver datos en formato JSON (útil para APIs y JavaScript).
from django.http import JsonResponse

# 'csrf_exempt': Desactiva una protección de seguridad de Django. 
# (Nota: Se usa aquí para simplificar llamadas desde JS, pero en producción se maneja de otra forma).
from django.views.decorators.csrf import csrf_exempt

# 'models': Nos ayuda a hacer cálculos en la base de datos (como sumas).
from django.db import models

# Importamos nuestras tablas (Modelos) definidas en models.py de esta app.
from .models import Cliente, Transaccion

# Importamos el modelo de Usuario de Django.
from django.contrib.auth.models import User

# 'json': Para poder leer datos que nos envían en formato texto (crudo) y convertirlos a Python.
import json

# 'Decimal': Para manejar dinero con precisión matemática (evita errores de los números flotantes).
from decimal import Decimal


# --- VISTA PRINCIPAL: DASHBOARD ---
# El símbolo '@' es un "decorador". Modifica la función de abajo.
# Aquí dice: "Solo ejecuta esta función si el usuario ha iniciado sesión".
@login_required
def dashboard(request):
    # --- CÁLCULO DE INGRESOS ---
    # Buscamos en la tabla Transaccion.
    # .filter(...): Solo las que sean del usuario actual y tipo 'INGRESO'.
    # .aggregate(total=models.Sum('monto')): Usa SQL para SUMAR la columna 'monto'.
    # ['total']: Extrae el resultado de la suma.
    # or 0: Si no hay ingresos, el resultado es 'None', así que lo convertimos a 0.
    total_ingresos = Transaccion.objects.filter(
        usuario=request.user, 
        tipo='INGRESO'
    ).aggregate(total=models.Sum('monto'))['total'] or 0
    
    # --- CÁLCULO DE GASTOS ---
    # Igual que arriba, pero filtrando por 'GASTO'.
    total_gastos = Transaccion.objects.filter(
        usuario=request.user, 
        tipo='GASTO'
    ).aggregate(total=models.Sum('monto'))['total'] or 0
    
    # --- BALANCE ---
    # Resta simple de Python para saber cuánto dinero queda.
    balance = total_ingresos - total_gastos
    
    # --- ÚLTIMAS TRANSACCIONES ---
    # Busca todas las transacciones del usuario.
    ultimas_transacciones = Transaccion.objects.filter(
        usuario=request.user
    # .order_by('-fecha'): Las ordena. El '-' significa de mayor a más reciente (descendente).
    # [:10]: Toma solo las primeras 10 (como un "limit").
    ).order_by('-fecha')[:10]
    
    # Preparamos el "contexto": Un diccionario con todos los datos calculados.
    # Esto es lo que enviaremos al HTML para que pueda mostrar los números.
    context = {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': balance,
        'ultimas_transacciones': ultimas_transacciones,
    }
    
    # Renderizamos la página HTML 'dashboard.html' y le pasamos los datos (context).
    return render(request, 'base/dashboard.html', context)


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
    # Trae todas las transacciones del usuario ordenadas por fecha.
    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')
    
    # Trae todos los clientes del usuario (probablemente para un selector desplegable en el HTML).
    clientes = Cliente.objects.filter(propietario=request.user)
    
    # Renderiza el HTML pasando ambas listas de datos.
    return render(request, 'base/transacciones.html', {
        'transacciones': transacciones,
        'clientes': clientes
    })


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
            descripcion=data.get('descripcion', '')
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