from django import forms
from .models import Processo

class ProcessoForm(forms.ModelForm):
    class Meta:
        model = Processo
        fields = ['cpf', 'cnpj', 'tipo_processo', 'status_processo','data_inicio','data_termino','descricao','responsavel']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control w-50', 'placeholder': 'Digite o CPF', 'required': False}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control w-50', 'placeholder': 'Digite o CNPJ', 'required': False}),
            'tipo_processo': forms.Select(attrs={'class': 'form-control w-50'}),
            'status_processo': forms.Select(attrs={'class': 'form-control w-50'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control w-50'}),
            'data_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control w-50'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control w-50'}),
            'responsavel': forms.Select(attrs={'class': 'form-control w-50'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf', '').strip()
        cnpj = cleaned_data.get('cnpj', '').strip()

        # Se o CPF ou CNPJ não for preenchido, definimos como None
        if not cpf:
            cleaned_data['cpf'] = None
        if not cnpj:
            cleaned_data['cnpj'] = None

        # Validação: pelo menos um dos campos deve ser preenchido
        if not cleaned_data['cpf'] and not cleaned_data['cnpj']:
            raise forms.ValidationError("É necessário preencher pelo menos o CPF ou o CNPJ.")

        # Se ambos os campos foram preenchidos, gera erro
        if cleaned_data['cpf'] and cleaned_data['cnpj']:
            raise forms.ValidationError("Preencha apenas o CPF ou o CNPJ, não ambos.")

        return cleaned_data