#!/usr/bin/python
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory, Blueprint
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, IntegerField
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
import datetime
from scanner import scan
import re


from kuripot_dashboard import dashboard_url

app = Flask(__name__)

getsweldo_url = Blueprint('getsweldo_url', __name__, template_folder='templates/get_sweldo')

now = datetime.datetime.now()
db_name = 'kuripot.db'
app.register_blueprint(dashboard_url)

class FORM_get_sweldo(Form):
    sahod_amount = IntegerField(" ")
    IP_class = SelectField( 'IP Classes', choices=(('C', 'Class C'), ('B', 'Class B'), ('A', 'Class A')))

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@getsweldo_url.route( '/get_sweldo', methods=['GET', 'POST'] )
@is_logged_in
def get_sweldo():
    form = FORM_get_sweldo(request.form)

    if request.method == "POST":
        sahod_amount  = request.form['sahod_amount']


        sahod_amount = re.sub('[!@#$%^&*()_+,<>/{}:"\`~]', "", str(sahod_amount) )
        sahod_amount = int(sahod_amount)

        if scan(sahod_amount)  == "MALICIOUS":
            flash ("Ma sulat ka nagd lg sweldo, hackon mo pako?", "danger")
            return render_template('get_sweldo.html', form=form)
        else:
            con = sqlite3.connect(db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            result = cur.execute( """ INSERT INTO salary_info ( salary_owner, salary_amount, salary_month_recv, salary_date_recv, salary_year_recv) VALUES (?,?,?,?,?)""", ( session['u_id'], sahod_amount, now.month, now.day, now.year,) )

            con.commit()
            cur.close()
            flash ('Salary Recived! Try to make it last! :)','success')
            return redirect( url_for('dashboard_url.dashboard') )
    return render_template('get_sweldo.html', form=form)


@getsweldo_url.route( '/_add_sweldo', methods=[ 'POST' ] )
def _add_sweldo():
    pass
