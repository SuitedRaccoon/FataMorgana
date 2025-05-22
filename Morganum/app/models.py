from . import db

class Produto(db.Model):
    __tablename__ = 'produtos'  # Adicione isso para ser explícito
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Produto {self.nome}>'