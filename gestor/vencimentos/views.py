from django.shortcuts import render, get_object_or_404, redirect
from .models import Vencimento
from clientes.models import Cliente
from empresas.models import Empresa
from .forms import VencimentoForm
from django.db.models import Q, OuterRef, Subquery, CharField, Case, When, Value
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'id_vencimento')
    direction = request.GET.get('direction', 'asc')

    # Subquery para cliente -> campo é "nome"
    cliente_nome = Cliente.objects.filter(cpf=OuterRef('cpf')).values('nome')[:1]
    empresa_nome = Empresa.objects.filter(cnpj=OuterRef('cnpj')).values('empresa')[:1]

    Vencimentos = Vencimento.objects.annotate(
        nome_cliente=Subquery(cliente_nome, output_field=CharField()),
        nome_empresa=Subquery(empresa_nome, output_field=CharField()),
        # Campo virtual Cliente/Empresa para ordenação
        cliente_empresa_order=Case(
            When(nome_cliente__isnull=False, then='nome_cliente'),
            default='nome_empresa',
            output_field=CharField()
        ),
        # Campo virtual CPF/CNPJ para ordenação
        cpf_cnpj_order=Case(
            When(cpf__isnull=False, then='cpf'),
            default='cnpj',
            output_field=CharField()
        )
    )

    # Filtro de busca
    if query:
        Vencimentos = Vencimentos.filter(
            Q(cpf__icontains=query) |
            Q(cnpj__icontains=query) |
            Q(nome_cliente__icontains=query) |
            Q(nome_empresa__icontains=query)
        )

    # Ordenação
    if order_by == 'cliente_empresa':
        order_field = 'cliente_empresa_order'
    elif order_by == 'cpf_cnpj':
        order_field = 'cpf_cnpj_order'
    else:
        order_field = order_by

    if direction == 'asc':
        Vencimentos = Vencimentos.order_by(order_field)
    else:
        Vencimentos = Vencimentos.order_by(f'-{order_field}')

    paginator = Paginator(Vencimentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index_vencimentos.html', {
        'page_obj': page_obj,
        'query': query,
        'order_by': order_by,
        'direction': direction
    })

@login_required
def adicionar_vencimento(request):
    if request.method == "POST":
        form = VencimentoForm(request.POST)
        cpf = request.POST.get('cpf', '').strip()
        cnpj = request.POST.get('cnpj', '').strip()

        if not cpf and not cnpj:
            form.add_error(None, "Preencha pelo menos o CPF ou o CNPJ.")

        if form.is_valid():
            # Antes de salvar, imprima os dados limpos do formulário
            print("Dados para salvar:", form.cleaned_data)

            # Salve o objeto
            form.save()

            return redirect('vencimentos:index_vencimento')
        else:
            # Se o formulário não for válido, mostre os erros
            print("Erro ao validar o formulário:", form.errors)
            return render(request, 'adicionar_vencimento.html', {'form': form})

    else:
        form = VencimentoForm()

    return render(request, 'adicionar_vencimento.html', {'form': form})

@login_required
def editar_vencimento(request, pk):
    vencimento = get_object_or_404(Vencimento, pk=pk)

    if request.method == "POST":
        form = VencimentoForm(request.POST, instance=vencimento)
        if form.is_valid():
            form.save()
            return redirect('vencimentos:index_vencimento')
    else:
        form = VencimentoForm(instance=vencimento)  # Passando o objeto existente para carregar os valores atuais

    return render(request, 'editar_vencimento.html', {'form': form, 'vencimento': vencimento})

@login_required
def excluir_vencimento(request, pk):
    vencimento = get_object_or_404(Vencimento, pk=pk)

    if request.method == 'POST':
        vencimento.delete()  # Aqui estava `Vencimento.delete()`, que é errado!
        return redirect('vencimentos:index_vencimento')

    return render(request, 'confirmar_exclusao_vencimento.html', {'vencimento': vencimento})

