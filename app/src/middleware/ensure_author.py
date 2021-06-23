from functools import wraps
from flask import session

from db import db
from middleware.error import AccessDeniedError, NotFoundError

def author_required(func):
    @wraps(func)
    def decorated(post_id):
        if session['role'] != 'admin':
            result = db.session.execute('''
                SELECT author
                FROM posts
                WHERE id = :id
            ''', { 'id': post_id }).fetchone()

            if not result:
                raise AccessDeniedError('You are not allowed to remove this post.')

            if result[0] != session['uid']:
                raise AccessDeniedError('You are not allowed to remove this post.')

        return func(post_id)
    return decorated

def admin_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if session['role'] != 'admin':
            raise NotFoundError('Page not found')

        return func(*args, **kwargs)
    return decorated
