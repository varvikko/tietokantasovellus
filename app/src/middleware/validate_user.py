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
    session['csrf_token'] = secrets.token_hex(16)

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

    result = db.session.execute('''
        SELECT name, role
        FROM users
        WHERE id = :id
    ''', { 'id': session['uid'] }).fetchone()

    username = result[0]
    role = result[1]

    if username:
        session['username'] = username

    session['role'] = role
