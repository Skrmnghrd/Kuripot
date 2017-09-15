#!/usr/bin/python
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory, Blueprint
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
#from string import maketrans
#from flask_debugtoolbar import DebugToolbarExtension
import cgi
import MySQLdb
from os import path, urandom, mkdir, listdir, remove
import uuid
from flask_uploads import UploadSet, configure_uploads, IMAGES
#from flask_wtf.file import FileField
from werkzeug import secure_filename
import imghdr
from flask_wtf.file import FileField
import multiprocessing
import sqlite3
import multiprocessing
import time

#urls and enpoints
from kuripot_dashboard import dashboard_url
from get_sweldo import getsweldo_url
from expenses_info import expenses_info_url
from savings import getsavings_url
from visualize import analytics_url

#custom scripts
from scanner import scan


banned_characters = ['%','<','"','\'','--+', '--', '=','<script>','</script']

app = Flask(__name__)
list_of_endpoints = [ getsweldo_url, dashboard_url, expenses_info_url, getsavings_url, analytics_url ]
for points in list_of_endpoints:
    app.register_blueprint(points)

db_name = 'kuripot.db'

"""
con = sqlite3.connect(db_name)
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute(str(query))
rows = cur.fetchall()
cur.close
"""

def cleaner(): #why not use crontab? bobo process itu haha use crontab 
    time.sleep(5)
    dirPath = "static/images"
    fileList = listdir(dirPath)
    for fileName in fileList:
        remove(path.join(dirPath, fileName))

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    return render_template('index.html')

class RegisterForm(Form):
   
    first_name = StringField('First Name: ', [validators.Length(min=1, max=50)])
    last_name = StringField('Last Name:', [validators.Length(min=1, max=50)])
    username = StringField('Username: ', [validators.Length(min=4, max=25)])
    email = StringField('Email: ', [validators.Length(min=6, max=50)])
    password = PasswordField('Password: ', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()


        first_name  = form.first_name.data
        last_name =  form.last_name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        scan_us = [first_name, last_name, username, email, form.password.data]
        scan_us_result = [ scan(x) for x in  scan_us ]

        if "MALICIOUS" in scan_us_result:
            flash ('Im here to help, Please don\'t harm me ;\'( ', 'danger')
            return redirect( url_for('register') )
         
        cur.execute("""SELECT user_username FROM owner_info where user_username=? """, (username,))
        exist = cur.fetchone()
        if exist is None:
            cur.execute( """INSERT INTO owner_info (first_name, last_name, user_email, user_username, user_password) VALUES (?,?,?,?,?)
            """, (first_name, last_name, email,  username, password) )
            con.commit()
            cur.close()

            flash('You are now registered! Please log in!', 'success')
            return redirect( url_for('login') )
        else:
            flash ('Username already exists, Please try a different one', 'danger')
    return render_template('register.html', form=form)
@app.route( '/login', methods=[ 'GET', 'POST' ] )        
def login():

    if request.method == "POST":
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        username = request.form['username']
        password_candidate = request.form['password']
        """
        for things in banned_characters:
            if things in username or things in password_candidate:
                flash ('You can just register. Why try to hack me? :( ', 'success')
                return redirect( url_for('register') )
            """
        if scan(username)  == "MALICIOUS" or scan(password_candidate) == "MALICIOUS":
            
                flash ('You can just register. Why try to hack me? :( ', 'danger')
                return redirect( url_for('register') )

        result = cur.execute( "SELECT * FROM owner_info WHERE user_username=?", ([username]) )
        exist = cur.fetchone()

        if exist is None:
            flash ('Username not found.', 'danger')
            return render_template('login.html')
        else:
            password = exist['user_password']
            
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['u_id'] = exist['id']
                session['user_salary'] = exist['salary_this_month']
                session['salary_left'] = exist['salary_left']

                cur.close()
                flash ('You are now logged in! Thank you', 'success')
                return redirect( url_for('dashboard_url.dashboard') )
            else:
                error = 'Login Invalid'
                return render_template('login.html', error=error)
            cur.close()
    return render_template('login.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


app.secret_key='thequickbrownfoxjumpedoverthelazydog'
clean = multiprocessing.Process(target=cleaner)
clean.start()
if __name__ == "__main__":
    app.secret_key='thequickbrownfoxjumpedoverthelazydog'
    app.run(port=8000, host="0.0.0.0", debug=True)
#expenses logs on exepenses area :) 