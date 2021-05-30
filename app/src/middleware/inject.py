from flask import session

from app import app
from db import db

@app.context_processor
def inject_boards():
    result = db.session.execute('''
        SELECT name, path
        FROM boards
    ''')

    boards = list(
        map(
            lambda t: { 'name': t[0], 'path': t[1] },
            result.fetchall()
        )
    )
    return dict(boards=boards, logged_in=('username' in session))

