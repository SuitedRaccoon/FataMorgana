from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import Livro, Editora, GeneroLiterario, LivroCompleto
from . import db
from datetime import datetime
import re

main_bp = Blueprint('main', __name__)
produto_bp = Blueprint('produto', __name__, url_prefix='/produtos')

@main_bp.route('/')
def index():
    return render_template('index.html')

@produto_bp.route('/')
def listar_produtos():
    # Usando a view LivroCompleto para obter informações relacionadas
    livros = LivroCompleto.query.all()
    return render_template('produtos.html', produtos=livros)

@produto_bp.route('/novo', methods=['GET', 'POST'])
def novo_produto():
    editoras = Editora.query.all()
    generos = GeneroLiterario.query.all()
    
    if request.method == 'POST':
        try:
            # Validação do ISBN-13
            isbn_13 = request.form['isbn_13']
            if not re.match(r'^\d{3}-\d-\d{5}-\d{3}-\d$', isbn_13):
                flash('Formato de ISBN-13 inválido. Use o formato: XXX-X-XXXXX-XXX-X', 'danger')
                return render_template('novo_produto.html', editoras=editoras, generos=generos)
            
            # Validação do ISBN-10 (se fornecido)
            isbn_10 = request.form.get('isbn_10', '')
            if isbn_10 and not re.match(r'^\d-\d{5}-\d{3}-\d$', isbn_10):
                flash('Formato de ISBN-10 inválido. Use o formato: X-XXXXX-XXX-X', 'danger')
                return render_template('novo_produto.html', editoras=editoras, generos=generos)
            
            novo_livro = Livro(
                isbn_13=isbn_13,
                isbn_10=isbn_10 if isbn_10 else None,
                titulo=request.form['titulo'],
                autor=request.form['autor'],
                editora_id=int(request.form['editora']),
                genero_literario_id=int(request.form['genero']),
                edicao=request.form.get('edicao'),
                impressao=request.form.get('impressao'),
                idioma=request.form.get('idioma', 'Português'),
                data_publicacao=datetime.strptime(request.form['data_publicacao'], '%Y-%m-%d').date() 
                               if request.form.get('data_publicacao') else None,
                quantidade_estoque=int(request.form['quantidade']),
                preco_livro=float(request.form['preco']),
                descricao=request.form.get('descricao', ''),
                numero_paginas=int(request.form['paginas']) if request.form.get('paginas') else None
            )
            
            db.session.add(novo_livro)
            db.session.commit()
            flash('Livro cadastrado com sucesso!', 'success')
            return redirect(url_for('produto.listar_produtos'))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Erro de valor: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar livro: {str(e)}', 'danger')
    
    return render_template('novo_produto.html', editoras=editoras, generos=generos)

@produto_bp.route('/editar/<isbn>', methods=['GET', 'POST'])
def editar_produto(isbn):
    livro = Livro.query.get_or_404(isbn)
    editoras = Editora.query.all()
    generos = GeneroLiterario.query.all()
    
    if request.method == 'POST':
        try:
            # Validação do ISBN-10 (se fornecido)
            isbn_10 = request.form.get('isbn_10', '')
            if isbn_10 and not re.match(r'^\d-\d{5}-\d{3}-\d$', isbn_10):
                flash('Formato de ISBN-10 inválido. Use o formato: X-XXXXX-XXX-X', 'danger')
                return render_template('editar_produto.html', produto=livro, editoras=editoras, generos=generos)
            
            livro.isbn_10 = isbn_10 if isbn_10 else None
            livro.titulo = request.form['titulo']
            livro.autor = request.form['autor']
            livro.editora_id = int(request.form['editora'])
            livro.genero_literario_id = int(request.form['genero'])
            livro.edicao = request.form.get('edicao')
            livro.impressao = request.form.get('impressao')
            livro.idioma = request.form.get('idioma', 'Português')
            livro.data_publicacao = datetime.strptime(request.form['data_publicacao'], '%Y-%m-%d').date() if request.form.get('data_publicacao') else None
            livro.quantidade_estoque = int(request.form['quantidade'])
            livro.preco_livro = float(request.form['preco'])
            livro.descricao = request.form.get('descricao', '')
            livro.numero_paginas = int(request.form['paginas']) if request.form.get('paginas') else None
            
            db.session.commit()
            flash('Livro atualizado com sucesso!', 'success')
            return redirect(url_for('produto.listar_produtos'))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Erro de valor: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar livro: {str(e)}', 'danger')
    
    return render_template('editar_produto.html', produto=livro, editoras=editoras, generos=generos)

@produto_bp.route('/excluir/<isbn>')
def excluir_produto(isbn):
    livro = Livro.query.get_or_404(isbn)
    
    try:
        # Verificar se o livro está em algum pedido antes de excluir
        if livro.pedidos:
            flash('Não é possível excluir este livro pois ele está associado a pedidos.', 'danger')
        else:
            db.session.delete(livro)
            db.session.commit()
            flash('Livro excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir livro: {str(e)}', 'danger')
    
    return redirect(url_for('produto.listar_produtos'))