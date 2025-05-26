# instance/config.py
import os

# Configurações do MySQL - ATUALIZE COM SEUS DADOS
MYSQL_USER = 'root'
MYSQL_PASSWORD = '#Guga2010'
MYSQL_HOST = 'localhost'  # ou IP do servidor
MYSQL_DB = 'morganum'

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '#Guga2010'  # Gere uma chave segura

# MySQL connection string => sqlalchemy.url = 'mysql+pymysql://gustavosaud@gmail.com:#Guga2010@localhost/morganum'