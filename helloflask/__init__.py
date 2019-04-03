from flask import Flask, g, Response, make_response, request, render_template, Markup, session, redirect, flash
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from helloflask.templates.init_db import init_database, db_session
from helloflask.models import Patient, Doctor
from flask import url_for


app = Flask(__name__)
app.debug = True  

app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/sign_in', methods=['GET'])
def show_sign_in():
    return render_template("form_extended.html")

@app.route('/sign_in', methods=['POST'])
def sign_in():
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    table = request.form.get('table')

    if table == 'patient':
        u = Patient.query.filter('email = :email and password = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
    else:
        u = Doctor.query.filter('email = :email and password = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()

    if u is not None:
        session['loginUser'] = { 'userid': u.id, 'name': u.name }
        if session.get('next'):
            next = session.get('next')
            del session['next']
            return redirect(next)
        return render_template("main.html")
        # return redirect('/')
    else:
        flash("해당 사용자가 없습니다!!")
        return render_template("form_extended.html")
        


@app.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")
    