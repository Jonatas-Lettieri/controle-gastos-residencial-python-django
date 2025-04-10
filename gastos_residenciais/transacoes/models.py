from django.db import models
import random
import string


# Função para gerar identificador aleatório
def gerar_identificador() -> str:
    ''' Gera um identificador aleatório de 10 caracteres '''
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


# Modelo para Usuário
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField(unique=True)
    identificador = models.CharField(max_length=10, default=gerar_identificador, unique=True)

    def __str__(self) -> str:
        return self.nome


# Modelo para Transações (receita ou despesa)
class Transacao(models.Model):
    TIPO_CHOICES = [
        ('despesa', 'Despesa'),
        ('receita', 'Receita'),
    ]
    descricao = models.CharField(max_length=255, verbose_name='descrição')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='usuário')

    def __str__(self) -> str:
        return f'{self.descricao} - {self.tipo} - {self.valor}'
    
