from django.contrib import admin
from .models import Usuario, Transacao

# Definição para personalizar a visualização dos usuários no admin
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'idade', 'identificador')  # Exibe essas colunas
    search_fields = ('nome', 'email')  # Campo de pesquisa para facilitar a busca de usuários
    list_filter = ('idade',)  # Filtro para buscar usuários por faixa etária

# Definição para personalizar a visualização das transações no admin
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'tipo', 'usuario', 'id')  # Exibe essas colunas
    search_fields = ('descricao', 'usuario__nome')  # Busca por descrição ou nome do usuário
    list_filter = ('tipo',)  # Filtro por tipo de transação (receita ou despesa)
    raw_id_fields = ('usuario',)  # Exibe o campo de usuário como um campo de busca, ao invés de uma lista longa

# Registra os modelos para aparecerem no admin com as personalizações
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Transacao, TransacaoAdmin)
