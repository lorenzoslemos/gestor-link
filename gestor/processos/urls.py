from django.urls import path
from . import views

app_name = 'processos'

urlpatterns = [
    path('', views.index, name='index_processo'),
    path('adicionar', views.adicionar_processo, name='adicionar_processo'),
    path('editar/<int:pk>/', views.editar_processo, name='editar_processo'),
    path('empresa/excluir/<int:pk>/', views.excluir_processo, name='excluir_processo'),
]