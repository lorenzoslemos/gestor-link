from django.contrib import admin
from .models import Empresa

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id_empresa','cnpj','empresa','id_regime','id_natureza')

admin.site.register(Empresa, EmpresaAdmin)