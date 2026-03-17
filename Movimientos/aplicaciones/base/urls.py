from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transacciones/', views.transacciones_lista, name='transacciones'),

    # APIs
    path('api/crear-transaccion/', views.crear_transaccion, name='crear_transaccion'),
    
    # APIs para ver, editar y eliminar (AGREGAR ESTAS 3)
    path('api/obtener-transaccion/<int:id>/', views.obtener_transaccion, name='obtener_transaccion'),
    path('api/editar-transaccion/<int:id>/', views.editar_transaccion, name='editar_transaccion'),
    path('api/eliminar-transaccion/<int:id>/', views.eliminar_transaccion, name='eliminar_transaccion'),
    
    # Importar Excel
    path('importar-excel/', views.importar_excel, name='importar_excel'),

    # Exportar Excel con Dashboard
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),

    # Deudas
    path('deudas/', views.deudas_lista, name='deudas'),
    path('api/crear-deuda/', views.crear_deuda, name='crear_deuda'),
    path('api/pagar-deuda/<int:id>/', views.pagar_deuda, name='pagar_deuda'),
    path('api/eliminar-deuda/<int:id>/', views.eliminar_deuda, name='eliminar_deuda'),

    # En urls.py — agregar esta línea junto a las otras de deuda:
    path('api/editar-deuda/<int:id>/', views.editar_deuda, name='editar_deuda'),

    # Registro y gestión de usuarios
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.mi_perfil, name='mi_perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
]