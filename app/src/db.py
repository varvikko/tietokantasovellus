import os
from flask_sqlalchemy import SQLAlchemy
from app import app

DATABASE_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace('://', 'ql://', 1) \
    if DATABASE_URL.startswith('postgres://') \
    else DATABASE_URL

db = SQLAlchemy(app)
