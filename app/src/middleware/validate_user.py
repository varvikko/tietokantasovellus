import secrets
from flask import session

from app import app
from db import db

def create_user():    
    result = db.session.execute('''
        INSERT INTO users
        DEFAULT VALUES
        RETURNING id
    ''')
    db.session.commit()
    uid = result.fetchone()[0]
    session['uid'] = uid

@app.before_request
def validate_user():
    if not 'uid' in session:
        create_user()

    result = db.session.execute('''
        SELECT id, name
        FROM users
        WHERE id = :id
    ''', { 'id': session['uid'] })
    count = result.fetchone()
    if count == 0:
        create_user()
