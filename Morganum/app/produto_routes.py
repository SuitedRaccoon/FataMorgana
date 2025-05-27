# app/produto_routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import Produto
from . import db

produto_routes = Blueprint('produto', __name__)

@produto_routes.route('/produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@produto_routes.route('/produtos/novo', methods=['GET', 'POST'])
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

@produto_routes.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
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

@produto_routes.route('/produtos/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('produto.listar_produtos'))