from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clientes/', views.clientes_lista, name='clientes'),
    path('transacciones/', views.transacciones_lista, name='transacciones'),
    
    # APIs
    path('api/crear-cliente/', views.crear_cliente, name='crear_cliente'),
    path('api/crear-transaccion/', views.crear_transaccion, name='crear_transaccion'),
    
    # APIs para ver, editar y eliminar (AGREGAR ESTAS 3)
    path('api/obtener-transaccion/<int:id>/', views.obtener_transaccion, name='obtener_transaccion'),
    path('api/editar-transaccion/<int:id>/', views.editar_transaccion, name='editar_transaccion'),
    path('api/eliminar-transaccion/<int:id>/', views.eliminar_transaccion, name='eliminar_transaccion'),
    
    # Importar Excel
    path('importar-excel/', views.importar_excel, name='importar_excel'),
]