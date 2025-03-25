from django.http import HttpResponse
from django.shortcuts import render
from .models import Reuniao
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    reunioes = Reuniao.objects.all()
    return render(request, 'index.html', {'reunioes': reunioes })

@login_required
def new(request):
    return HttpResponse("new, Reuniao!")