from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente
from .forms import ClienteForm
from django.db import connection
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'id_cliente')
    direction = request.GET.get('direction', 'asc')

    if query:
        clientes = Cliente.objects.filter(
            Q(nome__icontains=query) | Q(cpf__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()

    if direction == 'asc':
        clientes = clientes.order_by(order_by)
    else:
        clientes = clientes.order_by(f'-{order_by}')

    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index_clientes.html', {'page_obj': page_obj, 'query': query, 'order_by': order_by, 'direction': direction})

@login_required
def adicionar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO CLIENTE (cpf, nome, sobrenome) VALUES (%s, %s, %s)",
                    [dados['cpf'], dados['nome'], dados['sobrenome']]
                )

            return redirect('clientes:index_cliente')
    else:
        form = ClienteForm()

    return render(request, 'adicionar_cliente.html', {'form': form})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes:index_cliente')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes:index_cliente')

    return render(request, 'confirmar_exclusao_cliente.html', {'cliente': cliente})

