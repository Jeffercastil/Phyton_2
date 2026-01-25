# Aplicaciones/ingresos/admin.py
from django.contrib import admin
from .models import Cliente, Producto, DisponibilidadEntrega

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('documento_identidad', 'nombre', 'apellido', 'telefono', 'correo')
    search_fields = ('documento_identidad', 'nombre', 'apellido', 'correo')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_producto', 'nombre_producto', 'tipo', 'categoria', 'disponible')
    list_filter = ('tipo', 'categoria', 'disponible')
    search_fields = ('codigo_producto', 'nombre_producto')
    readonly_fields = ('codigo_producto',)

@admin.register(DisponibilidadEntrega)
class DisponibilidadEntregaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'dias_entrega', 'fecha_disponibilidad')
    search_fields = ('producto__nombre_producto',)