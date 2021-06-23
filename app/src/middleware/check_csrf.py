from functools import wraps
from flask import session, request

from middleware.error import AccessDeniedError

def check_csrf(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not 'csrf_token' in request.form or request.form['csrf_token'] != session['csrf_token']:
            raise AccessDeniedError('You are not allowed to post.')

        return func(*args, **kwargs)
    return decorated
