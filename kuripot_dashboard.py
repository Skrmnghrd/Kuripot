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
import re
import datetime

from scanner import scan
from visualize import *




now = datetime.datetime.now()
app = Flask(__name__)
dashboard_url = Blueprint('dashboard_url', __name__, template_folder='templates/dashboard')
db_name = 'kuripot.db'
app.register_blueprint(analytics_url)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


class FORM_dashboard(Form):
    galastuhan = StringField(' ', [validators.Length(min=1, max=100000)] )
    date_choice = [ (x, x ) for x  in range(1,32) ] 
    month_choice = [ (y, y) for y in range(1,13) ]
    year_choice = [ (y, y) for y in range(2017,2030) ]

    month_spent = SelectField(' ', choices=tuple(month_choice), default=(now.month) )
    end_month_spent = SelectField(' ', choices=tuple(month_choice),  default=(now.month) )
    date_spent = SelectField(' ', choices=tuple(date_choice), default=(now.day) )

    end_date_spent =SelectField(' ', choices=tuple(date_choice), default=(now.day) )

    year_spent = SelectField(' ', choices=tuple(year_choice), default=(now.year))

@dashboard_url.route( '/test_daw', methods=['GET', 'POST'] )
def test(awdawdawdawd):
    print ("awojdhawjkhdwajd", awdawdawdawd)

@dashboard_url.route( '/dashboard', methods=['GET', 'POST'] )
@is_logged_in
def dashboard():

    form = FORM_dashboard(request.form)
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute( """ SELECT salary_left, salary_this_month  from owner_info where id=?;
    """, ( session['u_id'], )  )
    result = cur.fetchall()
    cur.close()

    if request.method == 'POST':

        galastuhan = form.galastuhan.data
        month_spent = form.month_spent.data
        date_spent = form.date_spent.data
        end_date_spent = form.end_date_spent.data
        year_spent = form.year_spent.data
        end_month_spent = form.end_month_spent.data

        scan_us = [galastuhan, month_spent, date_spent, end_date_spent, year_spent, end_month_spent]

        scan_us_result = [ scan(x) for x in  scan_us]

        if "MALICIOUS" in scan_us_result:
            flash ('Im here to help, Please don\'t harm me ;\'( ', 'danger')
            return redirect( url_for('dashboard_url.dashboard') )
            

        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
        SELECT 
        expenses_amount, 
        expenses_category, 
        expenses_desc, 
        expenses_month_spent, 
        expenses_date_spent, 
        expenses_year_spent
        FROM expenses_info where expenses_info_owner=? and expenses_month_spent >= ? and expenses_month_spent <= ? and expenses_date_spent >=? and expenses_date_spent <= ? and expenses_year_spent=?;
        """, ( session['u_id'], month_spent, end_month_spent, date_spent, end_date_spent, year_spent, )  )
        information = cur.fetchall()
        cur.close()

        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(""" SELECT sum(expenses_amount) FROM expenses_info where expenses_info_owner=? and expenses_month_spent >= ? and expenses_month_spent <= ? and expenses_date_spent >=? and expenses_date_spent <= ? and expenses_year_spent=?;
        """, ( session['u_id'], month_spent, end_month_spent, date_spent, end_date_spent, year_spent, )  )
        tutal = cur.fetchone()
        cur.close()

        
        galastuhan = form.galastuhan.data
        month_spent = form.month_spent.data
        date_spent = form.date_spent.data
        end_date_spent = form.end_date_spent.data
        year_spent = form.year_spent.data
        end_month_spent = form.end_month_spent.data


        filename =  analytics(month_spent, end_month_spent, date_spent, end_date_spent, year_spent) 
        return render_template('dashboard.html', form=form, result=result, information=information, tutal=tutal, filename=filename)

    filename =  analytics(9, 9, 9, 9, 2017) 
    return render_template('dashboard.html', form=form, result=result, filename=filename)

