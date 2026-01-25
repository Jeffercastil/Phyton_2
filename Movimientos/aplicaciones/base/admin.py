from django.contrib import admin
from .models import Cliente, Transaccion


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['documento_identidad', 'nombre', 'apellido', 'correo']


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'monto', 'fecha', 'usuario']