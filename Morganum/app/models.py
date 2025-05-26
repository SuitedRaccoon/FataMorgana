from . import db
from datetime import datetime
from sqlalchemy import Enum, CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    cpf = db.Column(db.String(14), primary_key=True, 
                  comment='Formatado com pontos e traço (XXX.XXX.XXX-XX)')
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    tel = db.Column(db.String(20), nullable=True, 
                  comment='Formatado com código de país (+55 XX XXXX-XXXX)')
    senha = db.Column(db.String(60), nullable=False, 
                    comment='Hash bcrypt')
    data_nascimento = db.Column(db.Date, nullable=False)
    genero = db.Column(Enum('Masculino', 'Feminino', 'Não Binário', 'Outro', 
                         'Prefiro não informar', name='genero_enum'))
    criado_em = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    atualizado_em = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    cliente = db.relationship('Cliente', backref='usuario', uselist=False)
    funcionario = db.relationship('Funcionario', backref='usuario', uselist=False)
    enderecos = db.relationship('Endereco', backref='usuario', lazy=True)

    __table_args__ = (
        CheckConstraint('cpf ~ \'^[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}\\-[0-9]{2}$\'', 
                       name='chk_cpf_format'),
        CheckConstraint('email ~ \'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$\'', 
                       name='chk_email_format'),
        CheckConstraint('tel IS NULL OR tel ~ \'^\\+[0-9]{2} [0-9]{2} [0-9]{4,5}\\-[0-9]{4}$\'', 
                       name='chk_tel_format'),
        CheckConstraint('data_nascimento BETWEEN \'1900-01-01\' AND \'2100-01-01\'', 
                       name='chk_data_nascimento')
    )

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    id = db.Column(db.Integer, primary_key=True)
    creditos = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    ultimo_acesso = db.Column(db.TIMESTAMP, nullable=True)
    atualizado_em = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    usuario_cpf = db.Column(db.String(14), db.ForeignKey('usuario.cpf'), 
                       nullable=False, unique=True)

    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

    __table_args__ = (
        CheckConstraint('creditos >= 0', name='chk_creditos_positivos'),
    )

class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(45), nullable=False)
    salario = db.Column(db.Numeric(10, 2), nullable=False)
    comissao = db.Column(db.Numeric(10, 2), nullable=True, default=0.00)
    escala = db.Column(db.String(45), nullable=False)
    data_contratado = db.Column(db.Date, nullable=False)
    data_demissao = db.Column(db.Date, nullable=True)
    usuario_cpf = db.Column(db.String(14), db.ForeignKey('usuario.cpf'), 
                       nullable=False, unique=True)

    pedidos = db.relationship('Pedido', backref='funcionario', lazy=True)

    __table_args__ = (
        CheckConstraint('salario > 0', name='chk_salario_positivo'),
        CheckConstraint('comissao IS NULL OR comissao >= 0', name='chk_comissao_positiva'),
        CheckConstraint('data_demissao IS NULL OR data_demissao >= data_contratado', 
                       name='chk_datas_contratacao')
    )

class Editora(db.Model):
    __tablename__ = 'editora'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    cidade = db.Column(db.String(45), nullable=True)
    pais = db.Column(db.String(45), nullable=True)
    ano_fundacao = db.Column(db.SmallInteger, nullable=True)
    website = db.Column(db.String(255), nullable=True)

    livros = db.relationship('Livro', backref='editora', lazy=True)

    __table_args__ = (
        CheckConstraint('website IS NULL OR website ~ \'^(https?:\\/\\/)?([\\da-z\\.-]+)\\.([a-z\\.]{2,6})([\\/\\w \\.-]*)*\\/?$\'', 
                       name='chk_website_format'),
    )

class GeneroLiterario(db.Model):
    __tablename__ = 'genero_literario'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text, nullable=True)

    livros = db.relationship('Livro', backref='genero', lazy=True)

class Livro(db.Model):
    __tablename__ = 'livro'
    
    isbn_13 = db.Column(db.String(17), primary_key=True,
                     comment='Formatado com hífens (XXX-XX-XXXX-XXX-X)')
    isbn_10 = db.Column(db.String(14), nullable=True,
                     comment='Formatado com hífens (XXX-XX-XXXX-X)')
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora_id = db.Column(db.Integer, db.ForeignKey('editora.id'), nullable=False)
    genero_literario_id = db.Column(db.Integer, db.ForeignKey('genero_literario.id'), 
                          nullable=False)
    edicao = db.Column(db.String(45), nullable=True)
    impressao = db.Column(db.String(45), nullable=True)
    idioma = db.Column(db.String(45), nullable=False)
    data_publicacao = db.Column(db.Date, nullable=True)
    quantidade_estoque = db.Column(db.Integer, nullable=False, default=0)
    preco_livro = db.Column(db.Numeric(10, 2), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    numero_paginas = db.Column(db.Integer, nullable=True)
    criado_em = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    atualizado_em = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    pedidos = db.relationship('Pedido', secondary='livro_has_pedido', 
                            back_populates='livros')

    __table_args__ = (
        CheckConstraint('isbn_13 ~ \'^[0-9]{3}\\-[0-9]{1,2}\\-[0-9]{1,5}\\-[0-9]{1,5}\\-[0-9]$\'', 
                       name='chk_isbn13_format'),
        CheckConstraint('isbn_10 IS NULL OR isbn_10 ~ \'^[0-9]{1,5}\\-[0-9]{1,5}\\-[0-9]{1,6}\\-[0-9Xx]$\'', 
                       name='chk_isbn10_format'),
        CheckConstraint('preco_livro > 0', name='chk_preco_positivo'),
        CheckConstraint('data_publicacao IS NULL OR data_publicacao BETWEEN \'1500-01-01\' AND \'2100-01-01\'', 
                       name='chk_data_publicacao'),
        db.Index('idx_livro_titulo', 'titulo'),
        db.Index('idx_livro_autor', 'autor')
    )

class Pedido(db.Model):
    __tablename__ = 'pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, server_default=db.func.current_date())
    hora = db.Column(db.Time, nullable=False, server_default=db.func.current_time())
    metodo_envio = db.Column(Enum('Correio', 'Transportadora', 'Retirada', 'Digital', 
                                name='metodo_envio_enum'), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(Enum('Pendente', 'Processando', 'Enviado', 'Entregue', 'Cancelado', 
                          name='status_pedido_enum'), nullable=False, default='Pendente')
    cliente_usuario_cpf = db.Column(db.String(14), db.ForeignKey('cliente.usuario_cpf'), 
                                  nullable=False)
    funcionario_usuario_cpf = db.Column(db.String(14), db.ForeignKey('funcionario.usuario_cpf'), 
                                      nullable=True)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

    livros = db.relationship('Livro', secondary='livro_has_pedido', 
                           back_populates='pedidos')

    __table_args__ = (
        CheckConstraint('data BETWEEN \'2020-01-01\' AND \'2100-01-01\'', 
                       name='chk_data_pedido'),
        db.Index('idx_pedido_status', 'status'),
        db.Index('idx_pedido_data', 'data')
    )

class Endereco(db.Model):
    __tablename__ = 'endereco'
    
    id_end = db.Column(db.Integer, primary_key=True)
    nome_end = db.Column(db.String(45), nullable=False)
    morador = db.Column(db.String(45), nullable=False)
    pais = db.Column(db.String(45), nullable=False)
    cep = db.Column(db.String(10), nullable=False,
                  comment='Formatado com hífen (XXXXX-XXX)')
    estado = db.Column(Enum('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
                          'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
                          'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO',
                          name='estado_enum'), nullable=False)
    cidade = db.Column(db.String(45), nullable=False)
    logradouro = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(45), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    complemento = db.Column(db.String(45), nullable=True)
    referencia = db.Column(db.Text, nullable=True)
    envio = db.Column(db.Boolean, nullable=False, default=False)
    usuario_cpf = db.Column(db.String(14), db.ForeignKey('usuario.cpf'), nullable=False)
    criado_em = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    atualizado_em = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    __table_args__ = (
        CheckConstraint('cep ~ \'^[0-9]{5}\\-[0-9]{3}$\'', name='chk_cep_format'),
        CheckConstraint('numero > 0', name='chk_numero_positivo')
    )

class LivroHasPedido(db.Model):
    __tablename__ = 'livro_has_pedido'
    
    livro_isbn_13 = db.Column(db.String(17), db.ForeignKey('livro.isbn_13'), primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), primary_key=True)
    quant = db.Column(db.Integer, nullable=False)
    valor_unit = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False, 
                       server_default='quant * valor_unit')

    __table_args__ = (
        CheckConstraint('quant > 0', name='chk_quantidade_positiva'),
        CheckConstraint('valor_unit > 0', name='chk_valor_unit_positivo')
    )

class LivroCompleto(db.Model):
    __tablename__ = 'livros_completos'
    __table_args__ = {'info': {'is_view': True}}
    
    isbn_13 = db.Column(db.String(17), primary_key=True)
    isbn_10 = db.Column(db.String(14))
    titulo = db.Column(db.String(255))
    autor = db.Column(db.String(100))
    editora_id = db.Column(db.Integer)
    genero_literario_id = db.Column(db.Integer)
    edicao = db.Column(db.String(45))
    impressao = db.Column(db.String(45))
    idioma = db.Column(db.String(45))
    data_publicacao = db.Column(db.Date)
    quantidade_estoque = db.Column(db.Integer)
    preco_livro = db.Column(db.Numeric(10, 2))
    descricao = db.Column(db.Text)
    numero_paginas = db.Column(db.Integer)
    criado_em = db.Column(db.TIMESTAMP)
    atualizado_em = db.Column(db.TIMESTAMP)
    editora_nome = db.Column(db.String(100))
    editora_cidade = db.Column(db.String(50))
    editora_pais = db.Column(db.String(50))
    genero_literario = db.Column(db.String(100))
    genero_descricao = db.Column(db.Text)