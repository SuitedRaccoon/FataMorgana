from flask import Blueprint, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from .models import Livro
from . import db

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload_bp.route('/upload/<isbn>', methods=['POST'])
def upload_livro(isbn):
    if 'file' not in request.files:
        flash('Nenhum arquivo enviado', 'danger')
        return redirect(url_for('produto.detalhes_livro', isbn=isbn))
    
    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'danger')
        return redirect(url_for('produto.detalhes_livro', isbn=isbn))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{isbn}.jpg")
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'livros')
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))
        flash('Imagem do livro atualizada com sucesso!', 'success')
    
    return redirect(url_for('produto.detalhes_livro', isbn=isbn))