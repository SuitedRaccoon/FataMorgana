from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')
    
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Importa e registra blueprints
    from .routes import main_bp, produto_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(produto_bp)
    # Registre o blueprint de autenticação
    app.register_blueprint(auth_bp, url_prefix='/auth')

     if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    # Importa models explicitamente
    from . import models
    
    return app

