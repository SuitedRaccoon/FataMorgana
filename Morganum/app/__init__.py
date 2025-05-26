<<<<<<< HEAD
<<<<<<< HEAD
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
=======
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
>>>>>>> 2e91aa394c2944f2798d6141de9b12aee6bae13e
=======
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
>>>>>>> parent of 67b94d7 (Resolvendo conflitos)

db = SQLAlchemy()
migrate = Migrate()

<<<<<<< HEAD
<<<<<<< HEAD
class Livro(db.Model):
    __tablename__ = 'livro'
=======
def create_app():
    app = Flask(__name__)
    
    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
>>>>>>> 2e91aa394c2944f2798d6141de9b12aee6bae13e
=======
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')
>>>>>>> parent of 67b94d7 (Resolvendo conflitos)
    
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
<<<<<<< HEAD
<<<<<<< HEAD
    def imagem_url(self):
        return f"uploads/livros/{self.isbn_13}.jpg"
=======
    # Registra blueprints
=======
    # Importa e registra blueprints
>>>>>>> parent of 67b94d7 (Resolvendo conflitos)
    from .routes import main_bp, produto_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(produto_bp)
    
    # Importa models explicitamente
    from . import models
    
    return app

<<<<<<< HEAD
>>>>>>> 2e91aa394c2944f2798d6141de9b12aee6bae13e
=======
>>>>>>> parent of 67b94d7 (Resolvendo conflitos)
