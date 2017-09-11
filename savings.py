#!/usr/bin/python
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory, Blueprint
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
import cgi
import MySQLdb
from os import path, urandom, mkdir, listdir, remove
import uuid
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import secure_filename
import imghdr
from flask_wtf.file import FileField
import multiprocessing
import sqlite3
import datetime
from scanner import scan
import re



app = Flask(__name__)

getsavings_url = Blueprint('getsavings_url', __name__, template_folder='templates/savings')

now = datetime.datetime.now()
db_name = 'kuripot.db'


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
    sahod_amount = IntegerField(" ")
    IP_class = SelectField( 'IP Classes', choices=(('C', 'Class C'), ('B', 'Class B'), ('A', 'Class A')))


@getsavings_url.route( '/look_savings', methods=['GET', 'POST'] )
@is_logged_in
def look_at_savings():
	form = FORM_get_sweldo(request.form)

	con = sqlite3.connect(db_name)
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	result = cur.execute( """ select savings_saved_amount, savings_month_saved, savings_day_saved, savings_year_saved from savings_info where savings_owner=? """, ( session['u_id'], ) )	

	return render_template('loot_at_savings.html', form=form, result=result)