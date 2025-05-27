# instance/config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'morganum.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'morgana'  # Troque por uma chave segura

__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')
    
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Importa e registra blueprints
    from .routes import main_bp, produto_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(produto_bp)
    
    # Importa models explicitamente
    from . import models
    
    return app