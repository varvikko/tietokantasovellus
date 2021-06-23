from flask import render_template, request, redirect

from app import app
from controllers import boards
from controllers import users
from middleware.ensure_author import admin_required
from middleware.check_csrf import check_csrf
from middleware.error import InvalidDataError

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/admin/ban', methods=['POST'])
@admin_required
@check_csrf
def ban():
    uid = request.form['user-id']
    reason = request.form['reason']
    
    if not uid:
        raise InvalidDataError('User ID is missing.')

    if not reason:
        raise InvalidDataError('Ban reason is missing.')

    try:
        duration = int(request.form['duration'])
    except ValueError:
        raise InvalidDataError('Invalid ban duration.')

    users.ban(uid, reason, duration)

    return redirect('/admin')

@app.route('/unban', methods=['POST'])
@admin_required
@check_csrf
def unban():
    uid = request.form['user-id']

    if not uid:
        raise InvalidDataError('User ID is missing.')

    users.unban(uid)

    return redirect('/admin')

@app.route('/admin/new-board', methods=['POST'])
@admin_required
@check_csrf
def new_board():
    path = request.form['board-path']
    name = request.form['board-name']
    description = request.form['board-description']

    boards.create_board(path, name, description)

    return redirect('/admin')

@app.route('/admin/delete-board/<board_path>')
@admin_required
def delete_board(board_path):
    boards.delete_board(board_path)

    return redirect('/admin')

@app.route('/admin/permissions', methods=['POST'])
@admin_required
@check_csrf
def permissions():
    uid = request.form['user-id']
    state = request.form['permission']

    users.set_permission(uid, state)

    return redirect('/admin')
