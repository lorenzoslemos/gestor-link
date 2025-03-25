from django.urls import path
from . import views

app_name = 'vencimentos'

urlpatterns = [
    path('', views.index, name='index_vencimento'),
    path('adicionar/', views.adicionar_vencimento, name='adicionar_vencimento'),
    path('editar/<int:pk>/', views.editar_vencimento, name='editar_vencimento'),
    path('vencimento/excluir/<int:pk>/', views.excluir_vencimento, name='excluir_vencimento'),
]