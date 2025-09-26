from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static

app_name = 'gestor'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('autenticacao.urls', namespace='autenticacao')),
    path('', views.index, name='index'),
    path('clientes/', include('clientes.urls', namespace='clientes')),
    path('cobrancas/', include('cobrancas.urls', namespace='cobrancas')),
    path('empresas/', include('empresas.urls', namespace='empresas')),
    path('processos/', include('processos.urls', namespace='processos')),
    path('reunioes/', include('reunioes.urls', namespace='reunioes')),
    path('vencimentos/', include('vencimentos.urls', namespace='vencimentos'))
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)