from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import Produto
from . import db
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required


main_bp = Blueprint('main', __name__)
produto_bp = Blueprint('produto', __name__, url_prefix='/produtos')

@main_bp.route('/')
def index():
    return render_template('index.html')

@produto_bp.route('/')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@produto_bp.route('/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        
        novo_produto = Produto(nome=nome, descricao=descricao, preco=preco, quantidade=quantidade)
        db.session.add(novo_produto)
        db.session.commit()
        
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('produto.listar_produtos'))
    
    return render_template('novo_produto.html')

@produto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.preco = float(request.form['preco'])
        produto.quantidade = int(request.form['quantidade'])
        
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produto.listar_produtos'))
    
    return render_template('editar_produto.html', produto=produto)

@produto_bp.route('/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('produto.listar_produtos'))

# Importa o módulo de autenticação
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))