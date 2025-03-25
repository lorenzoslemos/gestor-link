from django.contrib import admin
from .models import Processo

class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('id_processo','cpf','cnpj','tipo_processo','status_processo','data_inicio','data_termino','descricao','responsavel')

admin.site.register(Processo, ProcessoAdmin)