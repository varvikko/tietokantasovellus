from flask import render_template
from app import app

class NotFoundError(Exception):
    pass

class InvalidDataError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class AccessDeniedError(Exception):
    pass

@app.errorhandler(404)
@app.errorhandler(NotFoundError)
def not_found_error(error):
    return render_template('error.html', title='Error 404', message=error), 404

@app.errorhandler(InvalidDataError)
def invalid_data_error(error):
    return render_template('error.html', title='Error 400', message=error), 400

@app.errorhandler(InvalidCredentialsError)
def invalid_credentials_error(error):
    return render_template('error.html', title='Error 401', message=error), 401

@app.errorhandler(AccessDeniedError)
def access_denied_error(error):
    return render_template('error.html', title='Error 403', message=error), 403
