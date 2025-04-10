from django.urls import path
from .views import (
    CadastroUsuarioView,
    UsuariosCadastradosView,
    CadastroTransacaoView,
    ConsultaTotaisView,
    RealizarTransacaoView,
    EditarUsuarioView,
    ExcluirUsuarioView,
)

# Paths da aplicação
urlpatterns = [
    path('cadastro_usuario/', CadastroUsuarioView.as_view(), name='cadastro_usuario'),
    path('usuarios_cadastrados/', UsuariosCadastradosView.as_view(), name='usuarios_cadastrados'),
    path('cadastro_transacao/', CadastroTransacaoView.as_view(), name='cadastro_transacao'),
    path('consulta_totais/', ConsultaTotaisView.as_view(), name='consulta_totais'),
    path('realizar_transacao/', RealizarTransacaoView.as_view(), name='realizar_transacao'),
    path('editar_usuario/<int:id>/', EditarUsuarioView.as_view(), name='editar_usuario'),
    path('excluir_usuario/<int:id>/', ExcluirUsuarioView.as_view(), name='excluir_usuario'),
]
