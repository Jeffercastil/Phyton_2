from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from .models import Producto
import json
# Create your views here.
@csrf_exempt
@require_http_methods(['GET', 'POST'])
def listar_productos(request):
    """Obtener lista de productos"""
    productos = Producto.objects.all()
    data=[]
    for producto in productos:
        data.append({
            'codigo_producto': producto.codigo_producto,
            'nombre_producto': producto.nombre_producto,
            'tipo': producto.tipo,
            'categoria': producto.categoria,
            'disponible': producto.disponible,
            'imagen': producto.imagen. url if producto.imagen else None
        })
    return JsonResponse({'productos': data})

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def crear_producto(request):
    """Crear un producto"""
    try:
        nombre=request.POST.get('nombre_producto')
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo')
        categoria = request.POST.get('categoria')
        disponible = request.POST.get('disponible', 'true') == 'true'
        imagen = request.FILES.get('imagen')

        producto = Producto(
            nombre_producto = nombre,
            descripcion = descripcion,
            tipo = tipo,
            categoria = categoria,
            disponible = disponible,
            imagen = imagen
        )
        producto.save()

        return JsonResponse({
            'Exitoso':True,
            'mensaje':'Producto creado con exito',
            'producto' : {
                'codigo_producto': producto.codigo_producto,
                'nombre_producto': producto.nombre_producto,
                'tipo': producto.tipo,
                'categoria': producto.categoria,
                'disponible': producto.disponible,
                'imagen': producto.imagen.url if producto.imagen else None
            }
        })
    except Exception as e:
        return JsonResponse({'Exitoso':False, 'error': str(e)},  status =400)


@csrf_exempt
@require_http_methods(['PUT', 'POST'])
def actualizar_producto(request, codigo):
    """Actualizar un producto existente"""
    try:
        producto = Producto.objects.get(codigo_producto=codigo)

        if request.method == 'PUT':
            data = json.loads(request.body)
            producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
            producto.descripcion = data.get('descripcion',producto.descripcion)
            producto.tipo = data.get('tipo', producto.tipo)
            producto.categoria = data.get('categoria', producto.categoria)
            producto.disponible = data.get('disponible', producto.disponible)
        else:
            producto.nombre_producto = request.POST.get('nombre_producto', producto.nombre_producto)
            producto.descripcion = request.POST.get('descripcion', producto.descripcion)
            producto.tipo = request.POST.get('tipo', producto.tipo)
            producto.categoria = request.POST.get('categoria', producto.categoria)
            producto.disponible = request.POST.get('disponible', producto.disponible)

        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']

        producto.save()

        return JsonResponse({
        'Exitoso':True,
        'mensaje':'Producto actualizado con exito',
        'producto' : {
            'codigo_producto': producto.codigo_producto,
            'nombre_producto': producto.nombre_producto,
            'tipo': producto.tipo,
            'categoria': producto.categoria,
            'disponible': producto.disponible,
            'imagen': producto.imagen.url if producto.imagen else None
         }
        })
    except Producto.DoesNotExist:
        return JsonResponse({'Exitoso':False, 'error':'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'Exitoso':False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(['DELETE', 'POST'])
def eliminar_producto(request, codigo):
    """Eliminar un producto"""
    try:
        producto = Producto.objects.get(codigo_producto=codigo)
        producto.delete()
        return JsonResponse({
            'Exitoso':True,
            'mensaje':'Producto eliminado con exito'
        })
    except Producto.DoesNotExist:
        return JsonResponse({'Exitoso':False, 'error':'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'Exitoso':False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(['GET'])
def obtener_producto(request,codigo):
    """Obtener un producto especifico"""
    try:
        producto = Producto.objects.get(codigo_producto=codigo)
        return JsonResponse({
             'Exitoso':True,
        'mensaje':'Producto actualizado con exito',
        'producto' : {
            'codigo_producto': producto.codigo_producto,
            'nombre_producto': producto.nombre_producto,
            'tipo': producto.tipo,
            'categoria': producto.categoria,
            'disponible': producto.disponible,
            'imagen': producto.imagen.url if producto.imagen else None
         }
        })
    except Producto.DoesNotExist:
        return JsonResponse({'Exitoso': False, 'error': 'Producto no encontrado'}, status=404)

