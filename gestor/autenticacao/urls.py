from django.urls import path
from . import views

app_name = 'autenticacao'

urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL para login
    path('logout/', views.logout_view, name='logout'),  # URL para logout
]
