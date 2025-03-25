from django import forms
from .models import Cobranca

class CobrancaForm(forms.ModelForm):
    valor = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control w-50'})
    )

    class Meta:
        model = Cobranca
        fields = ['cpf', 'cnpj', 'descricao', 'valor', 'data_vencimento', 'status_pagamento']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control w-50', 'required': False}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control w-50', 'required': False}),
            'descricao': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control w-50'}),
            'status_pagamento': forms.TextInput(attrs={'class': 'form-control w-50'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf', '').strip()
        cnpj = cleaned_data.get('cnpj', '').strip()

        if not cpf:
            cleaned_data['cpf'] = None
        if not cnpj:
            cleaned_data['cnpj'] = None

        if not cleaned_data['cpf'] and not cleaned_data['cnpj']:
            raise forms.ValidationError("É necessário preencher pelo menos o CPF ou o CNPJ.")

        # Se ambos os campos foram preenchidos, gera erro
        if cleaned_data['cpf'] and cleaned_data['cnpj']:
            raise forms.ValidationError("Preencha apenas o CPF ou o CNPJ, não ambos.")

        return cleaned_data
