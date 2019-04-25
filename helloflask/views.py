from helloflask import app
from flask import render_template, request, session, redirect, flash, Response, make_response, jsonify, url_for
from helloflask.models import Patient, Doctor, Pat_Usercol, UsercolMaster, Log, Discode, DisCode_Usercol, Doc_Pat
from sqlalchemy import func
from sqlalchemy.sql import select, insert
from helloflask.init_db import db_session
from sqlalchemy.orm import joinedload
from pprint import pprint
from datetime import date, datetime, timedelta
from helloflask.email import send_email
from itsdangerous import URLSafeTimedSerializer, SignatureExpired



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
def gatekeeper():
    print("111111111")
    if session.get('loginUser') == None:
        return redirect('/login')
    return render_template("application.html")

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
        u = Patient.query.filter('email = :email and password = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
        utype = False
    else:
        u = Doctor.query.filter('email = :email and password = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
        utype = True

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

@app.route('/log')
def log():
    
    uid = session['loginUser']["userid"]

    # petient column information
    ret = db_session.query(UsercolMaster).join(Pat_Usercol, UsercolMaster.id == Pat_Usercol.usercol_id).join(Patient, Patient.id == Pat_Usercol.pat_id).filter(Patient.id == uid).all()

    return render_template("log.html", uname=session['loginUser']["name"], ucol=ret) 



s = URLSafeTimedSerializer('The_Key') # QQQ secret key 바꾸기

@app.route('/sign_up', methods = ['GET'])
def sign_up():
        return render_template('sign_up3.html')

@app.route('/sign_up', methods=['POST'])
def sign_up_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if password != password2:
        flash("암호를 정확히 입력하세요!!")
        return render_template("sign_up3.html", email=email, name=name)
    else:
        p = Patient(email, name, password, True)
        try:
            token = s.dumps(email, salt = 'email_confirm')
            link = url_for('confirm_email', values = token, _external = True)
            send_email('로그포유 입니다.', email , link)
            
            db_session.add(p)
            db_session.commit() 
        except:
            db_session.rollback()

        flash("%s 님, 메일을 보냈으니 확인 해주세요." % name)
        return redirect("/login")



@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt= 'email_confirm', max_age = 100)

    except SignatureExpired:
        return '<h1>유효기간이 만료되었습니다. 다시 가입해주세요. </h1>'
    return redirect('/login')