import bcrypt
from flask import session

from db import db
from middleware.error import (
    InvalidCredentialsError,
    AccessDeniedError,
    InvalidDataError
)

ROUNDS=14

def user_exists(username):
    return db.session.execute('''
        SELECT COUNT(*) > 0
        FROM users
        WHERE name = :name
    ''', { 'name': username }).fetchone()[0]

def is_registered(uid):
    return db.session.execute('''
        SELECT role <> 'anon'
        FROM users
        WHERE id = :id
    ''', { 'id': uid }).fetchone()[0]

def is_banned(uid):
    return db.session.execute('''
        SELECT users.id IN (
            SELECT user_id
            FROM bans
            WHERE ends_at > NOW()
        )
        FROM users
        WHERE users.id = :uid
    ''', { 'uid': uid }).fetchone()[0]

def get_ban_details(uid):
    result = db.session.execute('''
        SELECT reason, ends_at
        FROM bans
        WHERE user_id = :uid AND ends_at > NOW()
    ''', { 'uid': uid }).fetchone()

    return {
        'reason': result[0],
        'ends_at': result[1]
    }

def ban(uid, reason, duration):
    db.session.execute('''
        INSERT INTO bans (user_id, reason, started_at, ends_at)
        VALUES (:user_id, :reason, current_timestamp, NOW() + INTERVAL ':duration DAYS')
    ''', { 'user_id': uid, 'reason': reason, 'duration': duration })
    db.session.commit()

def unban(uid):
    db.session.execute('''
        DELETE FROM bans
        WHERE user_id = :user_id
    ''', { 'user_id': uid })
    db.session.commit()

def set_permission(uid, state):
    db.session.execute('''
        UPDATE users
        SET role = :role
        WHERE id = :uid AND role <> 'anon'
    ''', { 'role': state, 'uid': uid })
    db.session.commit()

def register_user(username, password):
    if not username:
        raise InvalidDataError('Username can not be empty.')

    if not password or len(password) < 5:
        raise InvalidDataError('Minimum password length is 5.')

    if user_exists(username):
        raise InvalidDataError('Username is already taken.')

    uid = session['uid']
    if is_registered(uid):
        raise AccessDeniedError('You have already registered this account.')

    password_hash = bcrypt.hashpw(password, bcrypt.gensalt(rounds=ROUNDS)).decode()
    
    db.session.execute('''
        UPDATE users
        SET name = :name, passwd = :passwd, role = 'registered'
        WHERE id = :id
    ''', { 'name': username, 'passwd': password_hash, 'id': uid })
    db.session.commit()

def login(username, password):
    if 'username' in session:
        raise AccessDeniedError('You are already logged in.')

    result = db.session.execute('''
        SELECT name, passwd, id, role
        FROM users
        WHERE name = :name
    ''', { 'name': username }).fetchone()

    if not result:
        raise InvalidCredentialsError('Username or password is invalid.')

    user_exists = bool(result[0])
    if not user_exists:
        raise Exception('Username or password is invalid.')
    password_hash = result[1]

    correct_passwd = bcrypt.checkpw(password, password_hash.encode(encoding='UTF-8'))
    if not correct_passwd:
        raise Exception('Username or password is invalid.')

    session['username'] = username
    session['role'] = result[3]
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
        ), (
            SELECT COUNT(*)
            FROM hides
            WHERE user_id = :id
        )
    ''', { 'id': uid }).fetchone()

    post_count = result[0]
    thread_count = result[1]
    hidden_count = result[2]

    return {
        'post_count': post_count,
        'thread_count': thread_count,
        'hidden_count': hidden_count
    }
