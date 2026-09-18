from flask import render_template,redirect
from pkg import app

@app.route('/')
def landing():
    return render_template('care_landing.html')



@app.route('/login')
def login():
    return render_template('care_page.html')


@app.route('/reg')
def reg():
    return render_template('care_reg.html')


@app.route('/book')
def book():
    return render_template('book_appt.html')