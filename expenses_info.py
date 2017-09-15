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

expenses_info_url = Blueprint('expenses_info_url', __name__, template_folder='templates/expenses_info')


now = datetime.datetime.now()
db_name = 'kuripot.db'

app.register_blueprint(dashboard_url)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

class FORM_get_sweldo(Form):
    expense_amount = IntegerField(" ")
    expense_category = SelectField(' ', choices=( ('Transport', 'Transport'), ('Food', 'Food'), ('Beverage', 'Beverage'), ('Anastaisa\'s needs ', 'Anastaisa\'s needs '),('Groceries', 'Groceries'),('Bills', 'Bills'),('Health', 'Health'),('Others', 'Others'), ('Clothes','Clothes')  ) )
    expense_description = StringField("")

@expenses_info_url.route( '/expenses_info', methods=['GET', 'POST'] )
@is_logged_in
def expenses_info():
    form = FORM_get_sweldo(request.form)

    if request.method == "POST":

        expense_amount  = request.form['expense_amount']
        expense_amount = re.sub( '[!@#$%^&*()_+,<>/{}:"\`~]', "", str(expense_amount) )
        try:
            expense_amount = float(expense_amount)
        except:
            flash ("Please check for invalid characters", "danger")
            return render_template('expenses_info.html', form=form)


        expense_category = request.form['expense_category']

        expense_description = request.form['expense_description']

        expense_description = re.sub( '<>\\`', "", str(expense_description) )
        expense_description = str(expense_description)

        if scan(expense_amount)  == "MALICIOUS" or scan(expense_description) == "MALICIOUS":
            flash ("Please dont do anything to me :'(  Im here to help. :3", "danger")
            return render_template('expenses_info.html', form=form)
        else:

            con = sqlite3.connect(db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            result = cur.execute( """ INSERT INTO expenses_info ( 
                expenses_info_owner, 
                expenses_amount, 
                expenses_category, 
                expenses_desc, 
                expenses_month_spent, 
                expenses_date_spent, 
                expenses_year_spent) VALUES (?,?,?,?,?,?,?)
            """, ( session['u_id'], expense_amount, expense_category, expense_description, now.month, now.day, now.year,) )

            con.commit()
            cur.close()
            flash ('Payment Logged! reduced on current salary','danger') 
            #return redirect( url_for('dashboard_url.dashboard') )
            return redirect( url_for('expenses_info_url.expenses_info', form=form) )
    return render_template('expenses_info.html', form=form)