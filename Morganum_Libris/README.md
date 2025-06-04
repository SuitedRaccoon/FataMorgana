<div align="center">
  <img src="static/assets/morganum_libris_logo.png" height="350" alt="Morganum Libris">
</div>

# Morganum Libris

 Aplicação web "mobile first" em Flask feita para melhor organizar hábitos de leitura.
 ## Features:
  * Sistema de busca em banco de dados MySQL, fazendo consultas de forma simples e dinâmica;
  * Criação e costumização de listas de livros para ler futuramente;
  * Filas de leitura, podendo organizar livros em "Lendo Agora", "Planejado", "Concluído" e "Ignorado".
 
 ## Contents:
  * *app.py*: aplicação principal em python rodando o servidor Flask;
  * *models.py*: arquivo contendo todos o modelo de objeto padrão do banco de dados;
  * *popular_livros.py*: programa que utiliza API pública 'OpenLibary' para popular o banco de dados com informações sobre livros.

 ### Execução:
  * Baixar o diretório 'Morganum_Libris';
  * Instalar as extensões encontradas no arquivo 'requirements.txt';
  * Iniciar servidor MySQL e rodar o script 'ddl.sql' encontrado na pasta 'database';
  * No mesmo servidor, usando o banco 'libris', rodar o script 'dml.sql' encontrado na pasta 'database' para alimentar o banco;
  * No mesmo diretório 'Morganum_Libris':
    - criar arquivo 'config.py' contendo as seguintes informações:
      ```
      MYSQL_HOST = 'localhost' # (normalmente localhost)
      MYSQL_USER = 'seu_usuario_MySQL' # (normalmente root)
      MYSQL_PASSWORD = 'sua_senha' # (deixar '' caso não use senha)
      MYSQL_DB = 'libris'
      ```
  * (Opcional) Executar arquivo 'popular_livros.py' para alimentar o banco de dados em massa;
  * Executar arquivo app.py e abrir o endereço http apresentado no terminal.

<div align="center">
  <img src="static/assets/libris_icon.png" height="200" alt="Morganum Libris">
</div>
