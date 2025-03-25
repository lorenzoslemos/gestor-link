from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cpf', 'nome', 'sobrenome']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'nome': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'sobrenome': forms.TextInput(attrs={'class': 'form-control w-50'}),
        }


