"""
URL configuration for gastos_residenciais project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from transacoes import views


# Paths do projeto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('cadastro_usuario/', views.CadastroUsuarioView.as_view(), name='cadastro_usuario'),
    path('usuarios_cadastrados/', views.UsuariosCadastradosView.as_view(), name='usuarios_cadastrados'),
    path('cadastro_transacao/', views.CadastroTransacaoView.as_view(), name='cadastro_transacao'),
    path('consulta_totais/', views.ConsultaTotaisView.as_view(), name='consulta_totais'),
    path('realizar_transacao/', views.RealizarTransacaoView.as_view(), name='realizar_transacao'),
    path('transacoes/', include('transacoes.urls')),
]

# Personalizando a área de admin
admin.site.site_header = 'Administração de Controle de Gastos Residenciais'
admin.site.site_title = 'Bem-vindo(a) ao Controle de Gastos Residenciais'
admin.site.index_title = 'Sistema de Gerenciamento:'
