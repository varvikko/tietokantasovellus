import os
import sass
from flask import Flask, session

app = Flask(__name__, template_folder='templates')
app.url_map.strict_slashes = False
app.secret_key = os.environ['SECRET_KEY']

if os.environ['FLASK_ENV'] == 'development':
    sass.compile(dirname=('src/static/sass', 'src/static/css'))

from routes import user_routes
from routes import admin_routes
