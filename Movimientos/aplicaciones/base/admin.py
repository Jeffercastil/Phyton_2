from django.contrib import admin
from .models import Transaccion, Deuda, Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefono', 'ciudad', 'pais', 'fecha_registro']
    search_fields = ['usuario__username', 'usuario__email', 'telefono']
    list_filter = ['pais', 'ciudad']


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'monto', 'fecha', 'usuario', 'categoria']


@admin.register(Deuda)
class DeudaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'usuario', 'valor_total_a_pagar', 'activa', 'fecha_inicio']
    list_filter = ['activa', 'tipo']
    search_fields = ['nombre', 'descripcion']
