# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import main_routes, produto_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(produto_routes)
    
    return app