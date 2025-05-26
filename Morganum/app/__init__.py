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

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    
    cpf = db.Column(db.String(14), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    tel = db.Column(db.String(20))
    senha = db.Column(db.String(60), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(20))
    criado_em = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    atualizado_em = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), 
                            onupdate=db.func.current_timestamp())
    
    cliente = db.relationship('Cliente', backref='usuario', uselist=False)
    funcionario = db.relationship('Funcionario', backref='usuario', uselist=False)
    enderecos = db.relationship('Endereco', backref='usuario')
    
    def get_id(self):
        return self.cpf
    
    def set_password(self, password):
        self.senha = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.senha, password)

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
    
    isbn_13 = db.Column(db.String(18), primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora_id = db.Column(db.Integer, db.ForeignKey('editora.id'), nullable=False)
    genero_literario_id = db.Column(db.Integer, db.ForeignKey('genero_literario.id'), nullable=False)
    preco_livro = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False, default=0)
    # ... outros campos conforme seu schema
    
    editora = db.relationship('Editora', backref='livros')
    genero_literario = db.relationship('GeneroLiterario', backref='livros')
    
<<<<<<< HEAD
    def imagem_url(self):
        return f"uploads/livros/{self.isbn_13}.jpg"
=======
    # Registra blueprints
    from .routes import main_bp, produto_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(produto_bp)
    
    # Importa models explicitamente
    from . import models
    
    return app

>>>>>>> 2e91aa394c2944f2798d6141de9b12aee6bae13e
