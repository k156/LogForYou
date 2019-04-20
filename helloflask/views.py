from helloflask import app
from flask import render_template, request, session, redirect, flash, Response, make_response, jsonify
from helloflask.models import Patient, Doctor, Pat_Usercol, UsercolMaster, Log, Discode, DisCode_Usercol, Doc_Pat
from sqlalchemy import func
from sqlalchemy.sql import select, insert
from helloflask.init_db import db_session
from sqlalchemy.orm import joinedload

from pprint import pprint

from datetime import date, datetime, timedelta

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def login_check():
    if session['loginUser'] == None:
        return redirect('/login')
    else:
        # custom_res = Response("Custom Response", 200, {'test': 'ttt'})
        custom_res = {"code" : 200, "message" : "success"}
        return jsonify(custom_res)

app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

@app.route('/')
<<<<<<< HEAD
def main():
    return render_template("main.html")


=======
def gatekeeper():
    print("111111111")
    if session.get('loginUser') == None:
        return redirect('/login')
    return render_template("application.html")
>>>>>>> 7b3c566a5c70d3ff3fcc39ea35e5a4edfd540225

@app.route('/login')
def show_login():
    print("2222222222")
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    print("3333333333")
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    table = request.form.get('table')
    utype = ""

    if table == 'patient':
<<<<<<< HEAD
        u = Patient.query.filter(Patient.email == email and Patient.password == func.sha2(passwd, 256)).first()
    else:
        u = Doctor.query.filter(Doctor.email == email and Doctor.password == func.sha2(passwd, 256)).first()
=======
        u = Patient.query.filter('email = :email and password = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
        utype = False
    else:
        u = Doctor.query.filter('email = :email and password = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
        utype = True
>>>>>>> 7b3c566a5c70d3ff3fcc39ea35e5a4edfd540225

    if u is not None:
        print("313131313131")
        session['loginUser'] = { 'userid': u.id, 'name': u.name , 'utype' : utype}
        session['next'] = '/main'
        print(session)
        if session.get('next'):
            next = session.get('next')
            print(">>>>>", next)
            del session['next']
            return redirect(next)
    else:
        flash("해당 사용자가 없습니다!!")
        return redirect("/login")

@app.route('/logout')
def logout():
    print("444444444")
    if session.get('loginUser'):
        del session['loginUser']
    
    return redirect('/login')

@app.route('/main')
def main():

    s=session['loginUser']

    return render_template('main.html', utype=s['utype'], uname=s['name'])

@app.route('/main/r', methods=['POST'])
def read():

    doc_id = session['loginUser']['userid']
    p_list = Doc_Pat.query.filter(Doc_Pat.doc_id == doc_id).all()

    result = []

    for p in p_list:
        data = p.pat.get_json()
        
        result.append(data)
    
    return jsonify({'result': result})

@app.route('/main/s', methods=['POST'])
def search():
    print("6666666666")
    pat_id = request.form.get('s')
    
    p = Patient.query.filter(Patient.id == pat_id).first()
    print(p.get_json())

    return jsonify(p.get_json())

@app.route('/sign_up')
def sign_up():
    print("77777777777")
    return render_template('sign_up.html')

@app.route('/log')
def log():
    
    uid = session['loginUser']["userid"]

    # petient column information
    ret = db_session.query(UsercolMaster).join(Pat_Usercol, UsercolMaster.id == Pat_Usercol.usercol_id).join(Patient, Patient.id == Pat_Usercol.pat_id).filter(Patient.id == uid).all()

    return render_template("log.html", uname=session['loginUser']["name"], ucol=ret) 

