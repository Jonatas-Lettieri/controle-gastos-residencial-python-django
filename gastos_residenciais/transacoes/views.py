from django.shortcuts import render, redirect, get_object_or_404  # Funções para renderizar templates e buscar objetos
from django.views import View  # Classe base para as views
from django.contrib import messages  # Para exibir mensagens de sucesso e erro
from django.db.models import Sum  # Para somar valores em consultas

from .models import Usuario, Transacao
from .forms import UsuarioForm, TransacaoForm

# Página inicial
class HomeView(View):
    """
    View responsável por renderizar a página inicial do sistema.

    Método GET:
        Renderiza a página inicial.
    """
    def get(self, request):
        return render(request, 'home.html')


# Cadastro de usuário
class CadastroUsuarioView(View):
    """
    View para o cadastro de novos usuários.

    Método GET:
        Exibe o formulário de cadastro de um novo usuário.

    Método POST:
        Processa o envio do formulário, realizando o cadastro do usuário,
        com validação e exibição de mensagens de sucesso ou erro.
    """
    def get(self, request):
        form = UsuarioForm()  # Instancia o formulário vazio
        return render(request, 'cadastro_usuario.html', {'form': form})

    def post(self, request):
        form = UsuarioForm(request.POST)  # Preenche o formulário com os dados enviados pelo usuário
        if form.is_valid():
            form.save()  # Salva o novo usuário no banco de dados
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('usuarios_cadastrados')  # Redireciona para a lista de usuários cadastrados
        messages.error(request, 'Erro ao cadastrar usuário.')  # Caso ocorra erro no formulário
        return render(request, 'cadastro_usuario.html', {'form': form})


# Exibição de usuários cadastrados
class UsuariosCadastradosView(View):
    """
    View para exibir a lista de usuários cadastrados e seus totais de receitas,
    despesas e saldo.
   
    Método GET:
        Recupera todos os usuários e calcula seus totais de receitas, despesas e saldo.
    """
    def get(self, request):
        usuarios = Usuario.objects.all()  # Obtém todos os usuários cadastrados

        # Calcula os totais de receitas, despesas e saldo para cada usuário
        for usuario in usuarios:
            usuario.total_receitas = usuario.transacao_set.filter(tipo='receita').aggregate(Sum('valor'))['valor__sum'] or 0
            usuario.total_despesas = usuario.transacao_set.filter(tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
            usuario.saldo = usuario.total_receitas - usuario.total_despesas  # Calcula o saldo

        return render(request, 'usuarios_cadastrados.html', {'usuarios': usuarios})


# Cadastro de transações
class CadastroTransacaoView(View):
    """
    View para cadastrar novas transações financeiras (receitas, despesas ou transferências).

    Método GET:
        Exibe o formulário para cadastrar uma nova transação.

    Método POST:
        Processa o envio do formulário, realizando a validação de transações e
        salvando os dados, com mensagens de sucesso ou erro.
    """
    def get(self, request):
        form = TransacaoForm()  # Formulário vazio para transação
        return render(request, 'cadastro_transacao.html', {'form': form})

    def post(self, request):
        form = TransacaoForm(request.POST)  # Preenche o formulário com os dados enviados
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            valor = form.cleaned_data['valor']
            usuario = form.cleaned_data['usuario']

            # Verifica a idade do usuário para transações de receita
            if usuario.idade < 18 and tipo == 'receita':
                messages.error(request, 'Menores de 18 anos não podem realizar transações de receita.')
                return render(request, 'cadastro_transacao.html', {'form': form})

            # Calcula o saldo atual do usuário
            total_receitas = Transacao.objects.filter(usuario=usuario, tipo='receita').aggregate(Sum('valor'))['valor__sum'] or 0
            total_despesas = Transacao.objects.filter(usuario=usuario, tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
            saldo_atual = total_receitas - total_despesas

            # Verifica se a transação de despesa pode ser realizada com o saldo atual
            if tipo == 'despesa' or tipo == 'transferencia':
                if valor > saldo_atual:
                    messages.error(request, 'Saldo insuficiente para realizar esta transação.')
                    return render(request, 'cadastro_transacao.html', {'form': form})

            form.save()  # Salva a transação no banco de dados
            messages.success(request, 'Transação registrada com sucesso!')
            return redirect('consulta_totais')  # Redireciona para a página de consulta de totais
        messages.error(request, 'Erro ao registrar a transação.')  # Caso o formulário tenha erro
        return render(request, 'cadastro_transacao.html', {'form': form})


# Consulta de totais
class ConsultaTotaisView(View):
    """
    View para consultar o total de receitas, despesas e o saldo geral do sistema.

    Método GET:
        Calcula os totais de receitas e despesas, além do saldo geral do sistema.
    """
    def get(self, request):
        total_receitas = Transacao.objects.filter(tipo='receita').aggregate(total_receitas=Sum('valor'))['total_receitas'] or 0
        total_despesas = Transacao.objects.filter(tipo='despesa').aggregate(total_despesas=Sum('valor'))['total_despesas'] or 0
        saldo = total_receitas - total_despesas  # Calcula o saldo geral
        return render(request, 'consulta_totais.html', {'total_receitas': total_receitas, 'total_despesas': total_despesas, 'saldo': saldo})


# Realizar transação
class RealizarTransacaoView(View):
    """
    View para realizar uma transação financeira (receita, despesa ou transferência).

    Método GET:
        Exibe o formulário para realizar uma transação.

    Método POST:
        Processa a transação, validando o saldo do usuário e tipo de transação.
    """
    def get(self, request):
        return render(request, 'realizar_transacao.html')

    def post(self, request):
        usuario = request.user
        tipo = request.POST.get('tipo')
        valor = float(request.POST.get('valor'))  # Obtém o valor da transação

        # Verifica a idade do usuário para transações de receita
        if usuario.idade < 18 and tipo == 'receita':
            messages.error(request, 'Menores de 18 anos não podem realizar transações de receita.')
            return redirect('realizar_transacao')

        saldo_atual = usuario.saldo  # Obtém o saldo atual do usuário

        # Verifica se o tipo é despesa ou transferência e se o saldo é suficiente
        if tipo == 'despesa' and saldo_atual < valor:
            messages.error(request, 'Saldo insuficiente para realizar esta transação.')
            return redirect('realizar_transacao')

        # Cria a transação no banco de dados
        Transacao.objects.create(
            usuario=usuario,
            tipo=tipo,
            valor=valor,
            descricao=request.POST.get('descricao')
        )
        messages.success(request, 'Transação realizada com sucesso!')
        return redirect('consulta_totais')


# Edição de usuário
class EditarUsuarioView(View):
    """
    View para editar as informações de um usuário cadastrado.

    Método GET:
        Exibe o formulário para edição de um usuário específico.

    Método POST:
        Processa a edição dos dados do usuário.
    """
    def get(self, request, id):
        usuario = get_object_or_404(Usuario, id=id)  # Recupera o usuário pelo ID
        form = UsuarioForm(instance=usuario)  # Preenche o formulário com os dados do usuário
        return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

    def post(self, request, id):
        usuario = get_object_or_404(Usuario, id=id)  # Recupera o usuário pelo ID
        form = UsuarioForm(request.POST, instance=usuario)  # Preenche o formulário com os dados atualizados
        if form.is_valid():
            form.save()  # Salva as alterações do usuário
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('usuarios_cadastrados')  # Redireciona para a lista de usuários
        messages.error(request, 'Erro ao atualizar usuário.')  # Caso ocorra erro no formulário
        return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})


# Exclusão de usuário
class ExcluirUsuarioView(View):
    """
    View para excluir um usuário do sistema.

    Método GET:
        Exibe a confirmação de exclusão de um usuário.

    Método POST:
        Exclui o usuário selecionado.
    """
    def get(self, request, id):
        usuario = get_object_or_404(Usuario, id=id)  # Recupera o usuário pelo ID
        return render(request, 'confirmar_exclusao.html', {'usuario': usuario})

    def post(self, request, id):
        usuario = get_object_or_404(Usuario, id=id)  # Recupera o usuário pelo ID
        usuario.delete()  # Exclui o usuário do banco de dados
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('usuarios_cadastrados')  # Redireciona para a lista de usuários
    
