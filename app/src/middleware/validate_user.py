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
    session['role'] = 'anon'

def valid_user(uid):
    return db.session.execute('''
        SELECT :uid IN (SELECT id FROM users)
    ''', { 'uid': uid }).fetchone()[0]

@app.before_request
def validate_user():
    if not 'uid' in session:
        create_user()

    if not valid_user(session['uid']):
        session.clear()
        create_user()

    if session['role'] != 'anon' and not 'username' in session:
        result = db.session.execute('''
            SELECT name
            FROM users
            WHERE id = :id
        ''', { 'id': session['uid'] })

        username = result.fetchone()[0]
        session['username'] = username
