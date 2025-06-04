# FataMorgana
Repositório dedicado ao grupo FataMorgana para confecção de aplicativos ao longo do curso de Ciência da Computação do Centro Universitário UDF.

## Morganum Libris
<div align="center">
  <img src="Morganum_Libris/static/assets/morganum_libris_logo.png" height="350" alt="Morganum Libris">
</div>

 Aplicação web "mobile first" feita para melhor organizar hábitos de leitura.
 
 ### Features:
  * Sistema de busca em banco de dados MySQL, fazendo consultas de forma simples e dinâmica;
  * Criação e costumização de listas de livros para ler futuramente;
  * Filas de leitura, podendo organizar livros em "Lendo Agora", "Planejado", "Concluído" e "Ignorado".

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

## Morganum (Em Desenvolvimento)
<div align="center">
  <img src="Morganum/app/static/assets/morganum_logo.png" height="350" alt="Morganum">
</div>
 Aplicação web simulando um sistema de uma livraria.
 
 ### Features:
  * Sistema de login para clientes e funcionários;
  * Banco de dados com estoque da Livraria, assim como informações de usuários;
  * Sistema CRUD acessível a funcionarios;
  * Histórico de compras para clientes, além de sistema de pontos bonificando clientes com descontos de acordo com valor de suas compras;
  * Barra de busca que lista títulos com base em palavras-chave, nome de autor, gêneros, etc;
