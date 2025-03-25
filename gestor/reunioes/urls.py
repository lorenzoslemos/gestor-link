from django.urls import path
from . import views

app_name = 'reunioes'

urlpatterns = [
    path('', views.index),
    path('novaReuniao', views.new)
]