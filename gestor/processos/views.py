from django.shortcuts import render, get_object_or_404, redirect
from .models import Processo
from .forms import ProcessoForm
from clientes.models import Cliente
from empresas.models import Empresa
from django.db.models.functions import Coalesce
from django.db.models import Q, OuterRef, Subquery, CharField, Value
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'id_processo')
    direction = request.GET.get('direction', 'asc')

    # Subquery para Cliente (campo nome)
    cliente_nome = Cliente.objects.filter(cpf=OuterRef('cpf')).values('nome')[:1]

    # Subquery para Empresa (campo empresa)
    empresa_nome = Empresa.objects.filter(cnpj=OuterRef('cnpj')).values('empresa')[:1]

    # Anota os nomes e CPF/CNPJ combinados no queryset de Processos
    processos = Processo.objects.annotate(
        nome_cliente=Subquery(cliente_nome, output_field=CharField()),
        nome_empresa=Subquery(empresa_nome, output_field=CharField()),
        cpf_cnpj=Coalesce('cpf', 'cnpj'),  # CPF ou CNPJ
        cliente_empresa=Coalesce('nome_cliente', 'nome_empresa')  # Cliente ou Empresa
    )

    # Filtragem por query
    if query:
        processos = processos.filter(
            Q(cpf__icontains=query) |
            Q(cnpj__icontains=query) |
            Q(nome_cliente__icontains=query) |
            Q(nome_empresa__icontains=query)
        )

    # Ordenação
    if direction == 'asc':
        processos = processos.order_by(order_by)
    else:
        processos = processos.order_by(f'-{order_by}')

    # Paginação
    paginator = Paginator(processos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index_processos.html', {
        'page_obj': page_obj,
        'query': query,
        'order_by': order_by,
        'direction': direction
    })

@login_required
def adicionar_processo(request):
    if request.method == "POST":
        form = ProcessoForm(request.POST)
        cpf = request.POST.get('cpf', '').strip()
        cnpj = request.POST.get('cnpj', '').strip()

        if not cpf and not cnpj:
            form.add_error(None, "Preencha pelo menos o CPF ou o CNPJ.")

        if form.is_valid():
            # Antes de salvar, imprima os dados limpos do formulário
            print("Dados para salvar:", form.cleaned_data)

            # Salve o objeto
            form.save()

            return redirect('processos:index_processo')
        else:
            # Se o formulário não for válido, mostre os erros
            print("Erro ao validar o formulário:", form.errors)
            return render(request, 'adicionar_processo.html', {'form': form})

    else:
        form = ProcessoForm()

    return render(request, 'adicionar_processo.html', {'form': form})

@login_required
def editar_processo(request, pk):
    processo = get_object_or_404(Processo, pk=pk)
    if request.method == 'POST':
        form = ProcessoForm(request.POST, instance=processo)
        if form.is_valid():
            form.save()
            return redirect('processos:index_processo')
    else:
        form = ProcessoForm(instance=processo)
    return render(request, 'editar_processo.html', {'form': form, 'processo': processo})

@login_required
def excluir_processo(request, pk):
    processo = get_object_or_404(Processo, pk=pk)

    if request.method == 'POST':
        processo.delete()
        return redirect('processos:index_processo')

    return render(request, 'confirmar_exclusao_processo.html', {'processo': processo})

