from db import db
from middleware.error import InvalidDataError

def create_board(path, name, description):
    if not path:
        raise InvalidDataError('Invalid path')

    if not name:
        raise InvalidDataError('Invalid name')

    if not path.startswith('/'):
        path = '/' + path

    if not path.endswith('/'):
        path += '/'

    db.session.execute('''
        INSERT INTO boards (path, name, description)
        VALUES (:path, :name, :description)
    ''', { 'path': path, 'name': name, 'description': description })
    db.session.commit()

def get_board(path):
    result = db.session.execute('''
        SELECT name, path, description
        FROM boards
        WHERE path = :path
    ''', { 'path': f'/{path}/' })

    board = result.fetchone()

    return {
            'name': board[0],
            'path': board[1],
            'description': board[2],
    } if board else {}

def delete_board(path):
    if not path.startswith('/'):
        path = '/' + path

    if not path.endswith('/'):
        path += '/'

    db.session.execute('''
        DELETE FROM boards
        WHERE path = :path
    ''', { 'path': path })
    db.session.commit()

