from django.shortcuts import render, get_object_or_404, redirect
from .models import Empresa
from .forms import EmpresaForm
from django.db import connection
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


@login_required
def index(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'id_empresa')  # Valor padrão para ordenação
    direction = request.GET.get('direction', 'asc')  # Direção de ordenação (ascendente ou descendente)

    if query:
        empresas = Empresa.objects.filter(
            Q(empresa__icontains=query) | Q(cnpj__icontains=query)  # Busca no nome e no CNPJ
        )
    else:
        empresas = Empresa.objects.all()

    # Ordenação
    if direction == 'asc':
        empresas = empresas.order_by(order_by)
    else:
        empresas = empresas.order_by(f'-{order_by}')  # Ordenação descendente

    # Formatando o CNPJ para cada empresa
    for empresa in empresas:
        empresa.cnpj = formatar_cnpj(empresa.cnpj)  # Aplica a formatação ao CNPJ

    # Paginando as empresas: 10 empresas por página
    paginator = Paginator(empresas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index_empresas.html', {'page_obj': page_obj, 'query': query, 'order_by': order_by, 'direction': direction})


@login_required
def adicionar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data

            id_regime_valor = dados['id_regime'].id_regime
            id_natureza_valor = dados['id_natureza'].id_natureza

            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO "EMPRESA" (cnpj, empresa, id_regime, id_natureza) VALUES (%s, %s, %s, %s)',
                        [dados['cnpj'], dados['empresa'], id_regime_valor, id_natureza_valor]
                    )
                return redirect('empresas:index_empresa')

            except IntegrityError as e:
                # Verifica se a exceção é a violação de chave única
                if '2627' in str(e):
                    form.add_error('cnpj', 'Este CNPJ já está registrado.')
                else:
                    form.add_error(None, 'Ocorreu um erro ao tentar salvar a empresa.')

    else:
        form = EmpresaForm()

    return render(request, 'adicionar_empresa.html', {'form': form})

@login_required
def editar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('empresas:index_empresa')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'editar_empresa.html', {'form': form, 'empresa': empresa})

@login_required
def excluir_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)

    if request.method == 'POST':
        empresa.delete()
        return redirect('empresas:index_empresa')

    return render(request, 'confirmar_exclusao_empresa.html', {'empresa': empresa})


def formatar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))  # Remover qualquer caractere não numérico
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}" if len(cnpj) == 14 else cnpj
