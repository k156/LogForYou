from flask import Flask, g, Response, make_response, request, render_template, Markup
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from helloflask.templates.init_db import init_database, db_session
from flask import url_for


app = Flask(__name__)
app.debug = True  


@app.route('/')
def main():
    return render_template("application.html")


@app.route('/sign_in')
def sign_in():
    return render_template("form.html")


    
@app.route('/test')
def test():
    return render_template("main.html")