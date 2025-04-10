# gastos_residenciais (jonatas_saadi_de_almeida_lettieri)

## Introdução:
- Olá, meu nome é Jônatas Saadi de Almeida Lettieri, espero que esteja tudo bem com você. Então aqui estão algumas anotações importantes;

## Aviso importante sobre DEBUG = TRUE:
- DEBUG = True -> É igual a estar em ambiente de produção e os tratamentos de erro 404.html e 500.html não funcionam! Para funcionar esses tratamentos de erros tem que colocar no arquivo settings.py na variável DEBUG = False;

## Requisitos:
- O ideal é sempre criar um novo ambiente virtual para cada projeto (com o comando -> python3 -m venv "nome_do_ambiente_virtual") e ativá-lo (com o comando -> source "nome_do_ambiente_virtual"/bin/activate), após isso utilizar o comando para instalar todas as dependências que estão no arquivo requirements.txt (com o comando -> pip install -r requirements.txt);

- Criar um super usuário django para a area de administração django. Estando dentro do arquivo do projeto coloque no terminal o seguinte comando -> python manage.py createsuperuser. Após criar o super usuário django acesse -> http://127.0.0.1:8000/admin e faça o login para acessar a area administrativa;

- Criar um banco de dados PostgreSQL;

- É importante também que no arquivo settings.py na parte de configurações de DATABASE esteja com as informações certas do seu banco de dados;

## Execução do programa:
- Para executar o programa abra um terminal caminhe até o diretório do projeto (cd gastos_residenciais/) e digite essa sequência de 3 comandos:

   *1º - python manage.py makemigrations
    2º - python manage.py migrate
    3º - python manage.py runserver

- O primeiro comando é para fazer as migrações do projeto (* as migrações ja foram feitas para o arquivo de migrations, então agora esse comando só seria utilizado se tivesse que fazer alguma alteração no arquivo models.py), o segundo comando é para migrar os devidos dados de contrução de tabelas, colunas entre outras coisas para o banco de dados, e o terceiro comando é para iniciar um servidor rodando o projeto em localhost;

## Observação de Licença do projeto:
- Este projeto é pessoal e não deve ser reutilizado sem autorização;

## Observações finais:

- Esse projeto tem o intuito de demonstrar um sistema de controle de gastos residencial, utilizando Python, Django e PostgreSQL;

Obrigado!