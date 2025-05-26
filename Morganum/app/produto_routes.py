@produto_bp.route('/produtos')
def listar_produtos():
    search_query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 9
    
    query = Livro.query
    
    if search_query:
        query = query.filter(
            db.or_(
                Livro.titulo.ilike(f'%{search_query}%'),
                Livro.autor.ilike(f'%{search_query}%'),
                Livro.descricao.ilike(f'%{search_query}%')
            )
        )
    
    livros = query.join(GeneroLiterario).paginate(page=page, per_page=per_page)
    
    return render_template('produtos.html', livros=livros, search_query=search_query)

@produto_bp.route('/produtos/<isbn>')
def detalhes_livro(isbn):
    livro = Livro.query.get_or_404(isbn)
    return render_template('detalhes_livro.html', livro=livro)