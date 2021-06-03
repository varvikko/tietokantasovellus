import bcrypt
from flask import session

from db import db

ROUNDS=14

def register_user(username, password):
    uid = session['uid']
    registered = db.session.execute('''
        SELECT role <> 'anon'
        FROM users
        WHERE id = :id
    ''', { 'id': uid }).fetchone()[0]
    
    if registered:
        raise Exception('Already registered')

    password_hash = bcrypt.hashpw(password, bcrypt.gensalt(rounds=ROUNDS)).decode()
    
    db.session.execute('''
        UPDATE users
        SET name = :name, passwd = :passwd, role = 'registered'
        WHERE id = :id
    ''', { 'name': username, 'passwd': password_hash, 'id': uid })
    db.session.commit()

def login(username, password):
    if 'username' in session:
        raise Exception('Already logged in')

    result = db.session.execute('''
        SELECT name, passwd, id
        FROM users
        WHERE name = :name
    ''', { 'name': username }).fetchone()

    if not result:
        raise Exception('Invalid credentials')

    user_exists = bool(result[0])
    if not user_exists:
        raise Exception('User not found')
    password_hash = result[1]

    correct_passwd = bcrypt.checkpw(password, password_hash.encode(encoding='UTF-8'))
    if not correct_passwd:
        raise Exception('Invalid credentials')

    session['username'] = username
    session['uid'] = result[2] 

def logout():
    session.clear()

def get_stats(uid):
    result = db.session.execute('''
        SELECT (
            SELECT COUNT(posts)
            FROM users, posts
            WHERE users.id = :id AND author = :id
        ), (
            SELECT COUNT(posts)
            FROM users, posts
            WHERE users.id = :id AND author = :id and thread IS NULL
        )
    ''', { 'id': uid }).fetchone()

    post_count = result[0]
    thread_count = result[1]
    print(result, flush=True)

    return {
        'post_count': post_count,
        'thread_count': thread_count
    }
