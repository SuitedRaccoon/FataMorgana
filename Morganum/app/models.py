from . import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    telefone = db.Column(db.String(20))
    # Relacionamentos
    enderecos = db.relationship('Endereco', backref='cliente', lazy=True)
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

class Editora(db.Model):
    __tablename__ = 'editora'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True)
    telefone = db.Column(db.String(20))
    # Relacionamentos
    livros = db.relationship('Livro', backref='editora', lazy=True)

class Endereco(db.Model):
    __tablename__ = 'endereco'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    logradouro = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(50))
    bairro = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(9), nullable=False)

class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    data_admissao = db.Column(db.Date, default=datetime.utcnow)

class GeneroLiterario(db.Model):
    __tablename__ = 'genero_literario'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    # Relacionamentos
    livros = db.relationship('Livro', backref='genero', lazy=True)

class Livro(db.Model):
    __tablename__ = 'livro'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    ano_publicacao = db.Column(db.Integer)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=0)
    editora_id = db.Column(db.Integer, db.ForeignKey('editora.id'))
    genero_id = db.Column(db.Integer, db.ForeignKey('genero_literario.id'))
    # Relacionamento muitos-para-muitos com Pedido
    pedidos = db.relationship('Pedido', secondary='livro_has_pedido', back_populates='livros')

class Pedido(db.Model):
    __tablename__ = 'pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Processando')
    valor_total = db.Column(db.Float)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    # Relacionamento muitos-para-muitos com Livro
    livros = db.relationship('Livro', secondary='livro_has_pedido', back_populates='pedidos')

class LivroHasPedido(db.Model):
    __tablename__ = 'livro_has_pedido'
    
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), primary_key=True)
    quantidade = db.Column(db.Integer, default=1)
    preco_unitario = db.Column(db.Float)
    # Relacionamentos
    livro = db.relationship('Livro', backref='pedidos_associacao')
    pedido = db.relationship('Pedido', backref='livros_associacao')

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

class LivroCompleto(db.Model):
    __tablename__ = 'livros_completos'
    __table_args__ = {'info': {'is_view': True}}  # Indica que é uma view
    
    # Colunas principais do livro
    isbn_13 = db.Column(db.String(13), primary_key=True)
    isbn_10 = db.Column(db.String(10))
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora_id = db.Column(db.Integer, db.ForeignKey('editora.id'))
    genero_literario_id = db.Column(db.Integer, db.ForeignKey('genero_literario.id'))
    edicao = db.Column(db.Integer)
    impressao = db.Column(db.String(50))
    idioma = db.Column(db.String(30))
    data_publicacao = db.Column(db.Date)
    quantidade_estoque = db.Column(db.Integer, default=0)
    preco_livro = db.Column(db.Numeric(10, 2), nullable=False)
    descricao = db.Column(db.Text)
    numero_paginas = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Colunas da editora (join)
    editora_nome = db.Column(db.String(100))
    editora_cidade = db.Column(db.String(50))
    editora_pais = db.Column(db.String(50))
    
    # Colunas do gênero literário (join)
    genero_literario = db.Column(db.String(50))
    genero_descricao = db.Column(db.Text)
    
    # Método para representação
    def __repr__(self):
        return f'<LivroCompleto {self.titulo} - {self.isbn_13}>'
    
    # Método para serialização (API JSON)
    def to_dict(self):
        return {
            'isbn_13': self.isbn_13,
            'titulo': self.titulo,
            'autor': self.autor,
            'preco': float(self.preco_livro) if self.preco_livro else None,
            'editora': self.editora_nome,
            'genero': self.genero_literario,
            'estoque': self.quantidade_estoque
            # Adicione outros campos conforme necessário
        }