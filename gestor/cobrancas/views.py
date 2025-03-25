from django.shortcuts import render, get_object_or_404, redirect
from .models import Cobranca
from .forms import CobrancaForm
from django.db import connection
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'id_cobranca')
    direction = request.GET.get('direction', 'asc')

    if query:
        cobrancas = Cobranca.objects.filter(
            Q(cpf__icontains=query) | Q(cnpj__icontains=query)
        )
    else:
        cobrancas = Cobranca.objects.all()

    if direction == 'asc':
        cobrancas = cobrancas.order_by(order_by)
    else:
        cobrancas = cobrancas.order_by(f'-{order_by}')

    paginator = Paginator(cobrancas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index_cobrancas.html', {'page_obj': page_obj, 'query': query, 'order_by': order_by, 'direction': direction})

@login_required
def adicionar_cobranca(request):
    if request.method == 'POST':
        form = CobrancaForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO COBRANCA (cpf, cnpj, descricao, valor, data_vencimento, status_pagamento) VALUES (%s, %s, %s, %s, %s, %s)",
                    [dados['cpf'], dados['cnpj'], dados['descricao'], dados['valor'], dados['data_vencimento'], dados['status_pagamento']]
                )

            return redirect('cobrancas:index_cobranca')
    else:
        form = CobrancaForm()

    return render(request, 'adicionar_cobranca.html', {'form': form})

@login_required
def editar_cobranca(request, pk):
    cobranca = get_object_or_404(Cobranca, pk=pk)
    if request.method == 'POST':
        form = CobrancaForm(request.POST, instance=cobranca)
        if form.is_valid():
            form.save()
            return redirect('cobrancas:index_cobranca')
    else:
        form = CobrancaForm(instance=cobranca)
    return render(request, 'editar_cobranca.html', {'form': form, 'cobranca': cobranca})

@login_required
def excluir_cobranca(request, pk):
    cobranca = get_object_or_404(Cobranca, pk=pk)

    if request.method == 'POST':
        cobranca.delete()
        return redirect('cobrancas:index_cobranca')

    return render(request, 'confirmar_exclusao_cobranca.html', {'cobranca': cobranca})

