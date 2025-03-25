from django.contrib import admin
from .models import Vencimento

class VencimentoAdmin(admin.ModelAdmin):
    list_display = ('id_vencimento','cpf','cnpj','id_prazo','data_vencimento')

admin.site.register(Vencimento, VencimentoAdmin)