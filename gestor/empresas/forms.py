from django import forms
from .models import Empresa, RegimeTributario, NaturezaJuridica

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['cnpj', 'empresa', 'id_regime', 'id_natureza']
        widgets = {
            'cnpj': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'id_regime': forms.Select(),
            'id_natureza': forms.Select(),
        }

    id_regime = forms.ModelChoiceField(
        queryset=RegimeTributario.objects.all(),
        empty_label=None,
        label='Regime Tributário',
        widget=forms.Select(attrs={'class': 'form-control w-50'})
    )
    id_natureza = forms.ModelChoiceField(
        queryset=NaturezaJuridica.objects.all(),
        empty_label=None,
        label='Natureza Jurídica',
        widget = forms.Select(attrs={'class': 'form-control w-50'})
    )

