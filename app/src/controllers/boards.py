from db import db

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
