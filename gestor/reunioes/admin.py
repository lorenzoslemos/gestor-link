from django.contrib import admin
from .models import Reuniao

class ReuniaoAdmin(admin.ModelAdmin):
    list_display = ('id_reuniao','cliente','pauta','data_reuniao')

admin.site.register(Reuniao, ReuniaoAdmin)