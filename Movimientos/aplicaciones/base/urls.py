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
]