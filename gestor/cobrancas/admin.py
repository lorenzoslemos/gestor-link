from django.contrib import admin
from .models import Cobranca

class CobrancaAdmin(admin.ModelAdmin):
    list_display = ('id_cobranca','cpf','cnpj','descricao','valor','data_vencimento','status_pagamento')

admin.site.register(Cobranca, CobrancaAdmin)