from django import forms
from .models import Usuario, Transacao


# Formulário de usuário
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'idade', 'email']


# Formulário de transação
class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'tipo', 'usuario']
