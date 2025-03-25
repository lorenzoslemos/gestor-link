from django.urls import path
from .views import index
from . import views

app_name = 'empresas'

urlpatterns = [
    path('', views.index, name='index_empresa'),
    path('adicionar', views.adicionar_empresa, name='adicionar_empresa'),
    path('editar/<int:pk>/', views.editar_empresa, name='editar_empresa'),
    path('empresa/excluir/<int:pk>/', views.excluir_empresa, name='excluir_empresa'),  # Exclusão com confirmação
]