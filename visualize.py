#!/usr/bin/python
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory, Blueprint
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from os import path, urandom, mkdir, listdir, remove
import uuid
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import secure_filename
from matplotlib import style
from flask_wtf.file import FileField
import multiprocessing
import sqlite3
import uuid
import matplotlib.pyplot as plt
import threading

db_name = "kuripot.db"

"""

this is just for the graphs
"""
app = Flask(__name__)
analytics_url = Blueprint('analytics_url', __name__, template_folder='templates/analytics')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

class FORM_analytics(Form):
    galastuhan = StringField(' ', [validators.Length(min=1, max=100000)] )
    date_choice = [ (x, x ) for x  in range(1,32) ] 
    month_choice = [ (y, y) for y in range(1,13) ]
    year_choice = [ (y, y) for y in range(2017,2030) ]

    month_spent = SelectField(' ', choices=tuple(month_choice) )
    end_month_spent = SelectField(' ', choices=tuple(month_choice) )
    date_spent = SelectField(' ', choices=tuple(date_choice) )

    end_date_spent =SelectField(' ', choices=tuple(date_choice) )

    year_spent = SelectField(' ', choices=tuple(year_choice))


def get_sum(list_of_act, month_spent, end_month_spent, date_spent, end_date_spent, year_spent): #get some ahhaha
    return_this_dict = {}
    db_name = "kuripot.db"

    for keyss in list_of_act:

        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(""" 
        SELECT SUM(expenses_amount) 
        FROM expenses_info WHERE expenses_category = ? 
        AND expenses_info_owner= ? AND 
        expenses_month_spent >= ? AND
        expenses_month_spent <= ? AND
        expenses_date_spent >= ? AND
        expenses_date_spent <= ? AND
        expenses_year_spent = ?
        """, (keyss, session['u_id'], month_spent, end_month_spent, date_spent, end_date_spent, year_spent,) )

        result = cur.fetchall()
        cur.close()
        return_this_dict.update({str(keyss) : float(result[0][0]) })
        
    return return_this_dict

def process_data(act, slices): #this justs inserts into database
        style.use('fivethirtyeight')

        #fig, axes = plt.subplots()
        plt.pie(slices, labels=None, shadow=True, autopct='%0.1f%%')
        plt.title( 'Total Spent From/On \n Start Date here and End date' )
        plt.xlabel( str( sum( slices )) )
        plt.legend(labels=act) #sala ni. indi dapat alphabetical. dapat sorted by pinakamahal
        plt.tight_layout()
        pic_name = uuid.uuid4().hex + ".png"

        path = 'static/images/{0}'.format (pic_name)
        plt.savefig(path,transparent=True)
        
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(""" INSERT INTO data_charts (data_charts_owner, pie_chart, data_chart_date, data_chart_month, data_chart_year) VALUES (?,?,?,?,?)
        """, (3,pic_name,9,9,2017,))
        con.commit()
        cur.close()

@analytics_url.route( '/analytics', methods=['GET', 'POST'] )
@is_logged_in
def analytics(month_spent, end_month_spent, date_spent, end_date_spent, year_spent):
    form = FORM_analytics(request.form)
    if request.method == 'POST':
        db_name = "kuripot.db"
        """
        to add all contents of a list in python
        from functools import reduce
        reduce(lambda x,y: x + y, list_of_numbers)
        or sum(list_of_numbers)
        """
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""select DISTINCT 
        expenses_category FROM
        expenses_info WHERE
        expenses_info_owner= ? AND 
        expenses_month_spent >= ? AND
        expenses_month_spent <= ? AND
        expenses_date_spent >= ? AND
        expenses_date_spent <= ? AND
        expenses_year_spent = ?
        ORDER BY expenses_category
        """, (session['u_id'], month_spent, end_month_spent, date_spent, end_date_spent, year_spent,) )

        result = cur.fetchall()
        cur.close()

        act = []

        for things in result:
            act.append( (things[0]) )
        """
        #LIST COMPREHENSION KUNO PARA PRO ahhaa
        L = [[None], [123], [None], [151]]
        << list_indice[0] for variable in List if variable is not None >>
        """
        #a = [ x for x[0] in reversed(result) if x[0] is not None ]
        #a = list(filter( None.__ne__, [x[0] for x in reversed(result) ] ) )
        
        #slices = [*a]

        iter_me = get_sum(act, month_spent, end_month_spent, date_spent, end_date_spent, year_spent)
        act2 = []
        slices = []
        for keys, values in get_sum(act, month_spent, end_month_spent, date_spent, end_date_spent, year_spent).items():
            act2.append(keys)
            slices.append(values)



        #<value_when_condition_true> if <condition> else <value_when_condition_false> for value in list_name]
        #pleae design le fuken pie chart

        #colors act slices vars_to_query
        #q = multiprocessing.Queue()
        p = multiprocessing.Process( target=process_data, args=(act2, slices) )

        p.start()
        p.join()
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(""" select pie_chart from data_charts where data_charts_owner=3 ORDER BY id DESC """)
        a = cur.fetchone()
        #its a list a[0]
        cur.close()

        #return redirect( url_for( 'analytics_url.get_image', filename=str(a[0] ) ) )
        return str(a[0])
        #return send_from_directory( 'static/images', str(a[0]) )


@analytics_url.route('/_get_histogram_chart/<string:filename>', methods=['GET','POST'] )
@is_logged_in
def get_histogram_chart():
    pass
        #pass the varable like the one in the client database pelase work on this later 
@analytics_url.route( '/_get_image/<string:filename>', methods=['GET', 'POST'] )
@is_logged_in
def get_image(filename):
    return send_from_directory('static/images/', filename)
    #return filename

"""

select DISTINCT 
        expenses_category
        FROM
        expenses_info WHERE
        expenses_info_owner= 3 AND 
        expenses_month_spent >= 9 AND
        expenses_month_spent <= 9 AND
        expenses_date_spent >= 13 AND
        expenses_date_spent <= 13 AND
        expenses_year_spent = 2017
        ORDER BY sum(expenses_amount)


select sum(expenses_amount), expenses_category from expenses_info where expenses_category = (select DISTINCT expenses_category FROM expenses_info WHERE expenses_info_owner= 3 AND 
        expenses_month_spent >= 9 AND
        expenses_month_spent <= 9 AND
        expenses_date_spent >= 13 AND
        expenses_date_spent <= 13 AND
        expenses_year_spent = 2017
        ORDER BY expenses_category
)
UNION SELECT 
sum(expenses_amount), expenses_category from expenses_info where expenses_category = (select DISTINCT expenses_category FROM expenses_info WHERE expenses_info_owner= 3 AND 
        expenses_month_spent >= 9 AND
        expenses_month_spent <= 9 AND
        expenses_date_spent >= 13 AND
        expenses_date_spent <= 13 AND
        expenses_year_spent = 2017
        ORDER BY expenses_category
);

Bills		| sum(Bills)
Others		| sum(Others)
Transport	| sum(Transport)


300.0|Bills
please|populate
other|tings
here| if ok
"""