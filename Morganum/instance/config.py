import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/morganum_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'sua-chave-secreta-aqui'

# Configurações de upload
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB