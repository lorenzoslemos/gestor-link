from django.urls import path
from . import views

app_name = 'cobrancas'

urlpatterns = [
    path('', views.index, name='index_cobranca'),
    path('adicionar', views.adicionar_cobranca, name='adicionar_cobranca'),
    path('editar/<int:pk>/', views.editar_cobranca, name='editar_cobranca'),
    path('cobranca/excluir/<int:pk>/', views.excluir_cobranca, name='excluir_cobranca'),
]