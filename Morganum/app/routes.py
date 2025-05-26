from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import Livro, Editora, GeneroLiterario
from . import db
from datetime import datetime

main_bp = Blueprint('main', __name__)
produto_bp = Blueprint('produto', __name__, url_prefix='/produtos')

@main_bp.route('/')
def index():
    return render_template('index.html')

@produto_bp.route('/')
def listar_produtos():
    livros = Livro.query.all()
    return render_template('produtos.html', produtos=livros)

@produto_bp.route('/novo', methods=['GET', 'POST'])
def novo_produto():
    editoras = Editora.query.all()
    generos = GeneroLiterario.query.all()
    
    if request.method == 'POST':
        try:
            novo_livro = Livro(
                titulo=request.form['titulo'],
                isbn=request.form.get('isbn', ''),
                autor=request.form['autor'],
                ano_publicacao=int(request.form['ano']) if request.form['ano'] else None,
                preco=float(request.form['preco']),
                estoque=int(request.form['quantidade']),
                editora_id=int(request.form['editora']),
                genero_literario_id=int(request.form['genero']),
                descricao=request.form.get('descricao', ''),
                numero_paginas=int(request.form['paginas']) if request.form['paginas'] else None,
                edicao=int(request.form['edicao']) if request.form['edicao'] else None,
                idioma=request.form.get('idioma', 'Português'),
                criado_em=datetime.utcnow()
            )
            
            db.session.add(novo_livro)
            db.session.commit()
            flash('Livro cadastrado com sucesso!', 'success')
            return redirect(url_for('produto.listar_produtos'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar livro: {str(e)}', 'danger')
    
    return render_template('novo_produto.html', editoras=editoras, generos=generos)

@produto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    livro = Livro.query.get_or_404(id)
    editoras = Editora.query.all()
    generos = GeneroLiterario.query.all()
    
    if request.method == 'POST':
        try:
            livro.titulo = request.form['titulo']
            livro.autor = request.form['autor']
            livro.preco = float(request.form['preco'])
            livro.estoque = int(request.form['quantidade'])
            livro.editora_id = int(request.form['editora'])
            livro.genero_literario_id = int(request.form['genero'])
            livro.descricao = request.form.get('descricao', '')
            livro.numero_paginas = int(request.form['paginas']) if request.form['paginas'] else None
            livro.atualizado_em = datetime.utcnow()
            
            db.session.commit()
            flash('Livro atualizado com sucesso!', 'success')
            return redirect(url_for('produto.listar_produtos'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar livro: {str(e)}', 'danger')
    
    return render_template('editar_produto.html', produto=livro, editoras=editoras, generos=generos)

@produto_bp.route('/excluir/<int:id>')
def excluir_produto(id):
    livro = Livro.query.get_or_404(id)
    
    try:
        db.session.delete(livro)
        db.session.commit()
        flash('Livro excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir livro: {str(e)}', 'danger')
    
    return redirect(url_for('produto.listar_produtos'))