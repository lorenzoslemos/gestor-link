from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.index, name='index_cliente'),
    path('adicionar', views.adicionar_cliente, name='adicionar_cliente'),
    path('editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/excluir/<int:pk>/', views.excluir_cliente, name='excluir_cliente'),
]