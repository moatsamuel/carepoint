from flask import render_template
from pkg.AUTH import auth_bp

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')

@auth_bp.route('/reg')
def reg():
    return render_template('auth/register.html')