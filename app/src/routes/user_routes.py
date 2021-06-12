import secrets
from flask import render_template, request, make_response, session, redirect
from app import app

from controllers import boards
from controllers import images
from controllers import threads
from controllers import users
from controllers import posts
from db import db
from middleware.error import NotFoundError
from middleware.ensure_author import author_required

@app.route('/')
def index():

    popular_threads = threads.get_most_popular_threads(10)
    recent_threads = threads.get_most_recent_threads(10)

    return render_template('index.html',
        popular_threads=popular_threads,
        recent_threads=recent_threads)

@app.route('/thread/<thread_id>')
def thread(thread_id):

    thread_obj = threads.get_thread(thread_id)

    return render_template('thread_page.html', thread=thread_obj)

@app.route('/<board>')
@app.route('/<board>/<page>')
def board(board, page=1):
    board_obj = boards.get_board(board)
    if not board_obj:
        raise NotFoundError(f'Board named {board} does not exist.')

    offset = (int(page) - 1) * 10
    count = 10

    thread_list = threads.get_threads_from_board(
        board_obj['path'], offset, count
    )

    return render_template('board.html',
        board=board_obj,
        threads=thread_list,
        page=int(page))

@app.route('/hide/<thread_id>')
def hide(thread_id):
    threads.hide_thread(thread_id)

    return_to = request.args['returnto'] if 'returnto' in request.args else '/'
    return redirect(return_to)

@app.route('/new-thread', methods=['POST'])
def new_thread():
    image_id = images.add_image(request.files['image'])

    content = request.form['content']
    uid = session['uid']
    board = request.form['board']

    threads.create_thread(content, board, uid, image_id)

    return redirect(board)

@app.route('/reply', methods=['POST'])
def reply():
    image_id = images.add_image(request.files['image'])
    content = request.form['content']
    thread_id = request.form['thread']

    uid = session['uid']

    threads.reply(thread_id, content, uid, image_id)

    return redirect(f'/thread/{thread_id}')

@app.route('/edit-post/<post_id>', methods=['PUT'])
@author_required
def edit_post(post_id):
    content = request.json['content']

    posts.update(post_id, content)

    return redirect('/')

@app.route('/delete/<post_id>')
@author_required
def delete_post(post_id):
    posts.delete(post_id)

    return redirect('/')

@app.route('/self')
def self():
    return render_template('self.html', uid=session['uid'],
        username=session['username'] if 'username' in session else None)

@app.route('/self/stats')
def stats():
    uid = session['uid']
    stats = users.get_stats(uid)

    return render_template('stats.html', stats=stats)

@app.route('/self/settings')
def settings():
    return '/self/settings'

@app.route('/self/settings/save', methods=['POST'])
def save_settings():
    return '/self/settings/save'

@app.route('/self/logout')
def logout():
    users.logout()

    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] or ''
        password = request.form['password'] or ''
        users.login(username, password.encode(encoding='UTF-8'))

        return redirect('/')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users.register_user(username, password.encode(encoding='UTF-8'))

        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/i/<image>')
def get_image(image):
    obj = images.get_image(image)

    response = make_response(bytes(obj['data']))
    response.headers.set('Content-Type', obj['content_type'])
    return response

@app.route('/post/<post_id>')
def post(post_id):
    post = posts.get_post(post_id)

    return redirect(f'''/thread/{post['thread']}#{post['id']}''')
