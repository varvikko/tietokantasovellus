from flask import render_template
from app import app

@app.route('/')
def index():
    return '/'

@app.route('/<board>')
def board(board):
    return f'{board}'

@app.route('/<board>/<thread>')
def thread(board, thread):
    return f'/{board}/{thread}'

@app.route('/hide', methods=['POST'])
def hide():
    return '/hide'

@app.route('/new-thread', methods=['POST'])
def new_thread():
    return '/new-thread'

@app.route('/reply', methods=['POST'])
def reply():
    return '/reply'

@app.route('/edit-post', methods=['POST'])
def edit_post():
    return '/edit-post'

@app.route('/delete-thread', methods=['POST'])
def delete_thread():
    return '/delete-thread'

@app.route('/delete-post', methods=['POST'])
def delete_post():
    return '/delete-post'

@app.route('/self')
def self():
    return '/self'

@app.route('/self/stats')
def stats():
    return '/self/stats'

@app.route('/self/settings')
def settings():
    return '/self/settings'

@app.route('/self/settings/save', methods=['POST'])
def save_settings():
    return '/self/settings/save'

@app.route('/self/logout')
def logout():
    return '/self/logout'

@app.route('/login', methods=['POST'])
def login():
    return '/login'

@app.route('/i/<image>')
def get_image(image):
    return f'/i/{image}'
