from flask import render_template
from app import app

@app.errorhandler(Exception)
def error(e):
    return render_template('error.html', error=e)
