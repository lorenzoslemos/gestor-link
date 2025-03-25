from django.shortcuts import render, get_object_or_404, redirect
from .models import Vencimento
from .forms import VencimentoForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'id_vencimento')
    direction = request.GET.get('direction', 'asc')

    if query:
        Vencimentos = Vencimento.objects.filter(
            Q(cpf__icontains=query) | Q(cnpj__icontains=query)
        )
    else:
        Vencimentos = Vencimento.objects.all()

    if direction == 'asc':
        Vencimentos = Vencimentos.order_by(order_by)
    else:
        Vencimentos = Vencimentos.order_by(f'-{order_by}')

    paginator = Paginator(Vencimentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index_vencimentos.html', {'page_obj': page_obj, 'query': query, 'order_by': order_by, 'direction': direction})

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

