import os

<<<<<<< HEAD
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/morganum_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'sua-chave-secreta-aqui'

# Configurações de upload
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
=======
# Configurações do MySQL - ATUALIZE COM SEUS DADOS
MYSQL_USER = 'root'
MYSQL_PASSWORD = '#Guga2010'
MYSQL_HOST = 'localhost'  # ou IP do servidor
MYSQL_DB = 'morganum'

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '#Guga2010'  # Gere uma chave segura

# MySQL connection string => sqlalchemy.url = 'mysql+pymysql://gustavosaud@gmail.com:#Guga2010@localhost/morganum'
>>>>>>> 2e91aa394c2944f2798d6141de9b12aee6bae13e
