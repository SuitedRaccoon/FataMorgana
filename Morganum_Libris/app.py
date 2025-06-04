# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import MySQLdb
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)

def conectar_bd():
    """Connect to MySQL and return the connection."""
    return MySQLdb.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        passwd=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset='utf8mb4'
    )

@app.route('/')
def inicio():

    db = conectar_bd()
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    user_id = 1  

    cur.execute("""
        SELECT b.id, b.title AS titulo, b.author AS autor,
               b.genre AS genero, b.year_published AS ano_publicacao,
               ub.status, ub.queue_position
          FROM user_books ub
          JOIN books b ON b.id = ub.book_id
         WHERE ub.user_id = %s
         ORDER BY
           CASE ub.status
             WHEN 'reading'   THEN 1
             WHEN 'planned'   THEN 2
             WHEN 'completed' THEN 3
             WHEN 'skipped'   THEN 4
           END,
           ub.queue_position
    """, (user_id,))
    rows = cur.fetchall()
    livros_por_status = {'reading': [], 'planned': [], 'completed': [], 'skipped': []}
    for r in rows:
        livros_por_status[r['status']].append(r)

    cur.execute("""
        SELECT sl.id    AS lista_id,
            sl.name  AS nome_lista,
            b.id     AS livro_id,
            b.title  AS titulo,
            b.author AS autor,
            b.genre  AS genero,
            b.year_published AS ano_publicacao,
            b.isbn   AS isbn
        FROM saved_lists sl
        LEFT JOIN saved_list_books slb ON sl.id = slb.list_id
        LEFT JOIN books b ON b.id = slb.book_id
        WHERE sl.user_id = %s
        ORDER BY sl.id, b.title
    """, (user_id,))
    rows = cur.fetchall()

    listas_dict = {}
    for r in rows:
        lid = r['lista_id']
        if lid not in listas_dict:
            listas_dict[lid] = {
                'id': lid,
                'nome': r['nome_lista'],
                'livros': []
            }

        if r['livro_id'] is not None:
            listas_dict[lid]['livros'].append({
                'id': r['livro_id'],
                'titulo': r['titulo'],
                'autor': r['autor'],
                'genero': r['genero'],
                'ano_publicacao': r['ano_publicacao'],
                'isbn': r['isbn']
            })

    listas_salvas = list(listas_dict.values())


    cur.close()
    db.close()

    return render_template('index.html',
                           livros_por_status=livros_por_status,
                           listas_salvas=listas_salvas)

@app.route('/api/buscar')
def api_buscar():
    q = request.args.get('q','').strip()
    if len(q) < 2:
        return jsonify([])
    db = conectar_bd()
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    like = f"%{q}%"
    cur.execute("""
        SELECT id, title AS titulo, author AS autor,
               genre AS genero, year_published AS ano_publicacao, isbn
          FROM books
         WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s
         ORDER BY title
         LIMIT 50
    """, (like, like, like))
    results = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(results)

@app.route('/api/listas')
def api_listas():
    user_id = 1  # Substituir por controle de sessão real no futuro
    db = conectar_bd()
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT name FROM saved_lists WHERE user_id = %s ORDER BY name", (user_id,))
    listas = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(listas)

@app.route('/add_to_queue/<int:book_id>', methods=['POST'])
def add_to_queue(book_id):
    """Adiciona livro à fila com status escolhido e posição."""
    user_id = 1
    posicao = request.form.get('posicao', 'end')
    status = request.form.get('status', 'planned')

    db = conectar_bd()
    cur = db.cursor()

    if posicao == 'start':
        cur.execute("""
            UPDATE user_books
               SET queue_position = queue_position + 1
             WHERE user_id = %s
        """, (user_id,))
        nova_pos = 1
    else:
        cur.execute("SELECT COALESCE(MAX(queue_position),0)+1 FROM user_books WHERE user_id=%s", (user_id,))
        nova_pos = cur.fetchone()[0]

    cur.execute("""
        INSERT IGNORE INTO user_books (user_id, book_id, status, queue_position)
        VALUES (%s, %s, %s, %s)
    """, (user_id, book_id, status, nova_pos))

    db.commit()
    cur.close()
    db.close()
    return ('', 204)

@app.route('/listas/criar', methods=['GET','POST'])
def criar_lista():
    """Create a new saved list (public/private)."""
    user_id = 1
    if request.method == 'POST':
        name = request.form['name']
        public = bool(request.form.get('is_public'))
        db = conectar_bd()
        cur = db.cursor()
        cur.execute("INSERT INTO saved_lists (user_id,name,is_public) VALUES (%s,%s,%s)",
                    (user_id, name, public))
        db.commit()
        cur.close()
        db.close()
        return redirect(url_for('inicio'))
    return render_template('create_list.html')

@app.route('/listas/adicionar_por_nome', methods=['POST'])
def adicionar_por_nome():
    user_id   = 1
    book_id   = request.form['book_id']
    list_name = request.form['list_name']

    db = conectar_bd()
    cur = db.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("SELECT id FROM saved_lists WHERE user_id=%s AND name=%s", (user_id, list_name))
    row = cur.fetchone()
    if row:
        list_id = row['id']

        cur.execute("""
            SELECT COALESCE(MAX(position),0)+1 AS proxima_pos
              FROM saved_list_books
             WHERE list_id=%s
        """, (list_id,))
        pos = cur.fetchone()['proxima_pos']

        cur.execute("""
            INSERT IGNORE INTO saved_list_books (list_id, book_id, position)
            VALUES (%s, %s, %s)
        """, (list_id, book_id, pos))

        db.commit()

    cur.close()
    db.close()
    return ('', 204)

@app.route('/atualizar_status/<int:user_id>/<int:book_id>/<status>')
def atualizar_status(user_id, book_id, status):
    """Update a book’s status in user_books."""
    db = conectar_bd()
    cur = db.cursor()
    cur.execute("UPDATE user_books SET status=%s WHERE user_id=%s AND book_id=%s",
                (status, user_id, book_id))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('inicio'))

@app.route('/listas/remover/<int:lista_id>/<int:livro_id>', methods=['POST'])
def remover_da_lista(lista_id, livro_id):
    """
    Remove a book from a saved list.
    """
    db = conectar_bd()
    cur = db.cursor()
    cur.execute(
        "DELETE FROM saved_list_books WHERE list_id=%s AND book_id=%s",
        (lista_id, livro_id)
    )
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('inicio'))

@app.route('/listas/excluir/<int:lista_id>', methods=['POST'])
def excluir_lista(lista_id):
    user_id = 1
    db = conectar_bd()
    cur = db.cursor()
    
    # Remove livros da lista
    cur.execute("DELETE FROM saved_list_books WHERE list_id = %s", (lista_id,))
    
    # Remove a lista em si
    cur.execute("DELETE FROM saved_lists WHERE id = %s AND user_id = %s", (lista_id, user_id))
    
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('inicio'))

@app.route('/fila/limpar/<status>', methods=['POST'])
def limpar_etapa_fila(status):
    user_id = 1
    if status not in ['reading', 'planned', 'completed', 'skipped']:
        return "Status inválido", 400

    db = conectar_bd()
    cur = db.cursor()
    cur.execute("DELETE FROM user_books WHERE user_id=%s AND status=%s", (user_id, status))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('inicio'))


if __name__ == '__main__':
    app.run(debug=True)
