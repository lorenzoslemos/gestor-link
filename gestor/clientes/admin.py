from django.contrib import admin
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente','cpf','nome','sobrenome')

admin.site.register(Cliente, ClienteAdmin)