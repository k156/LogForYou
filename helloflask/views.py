from helloflask import app
from flask import render_template, request, session, redirect, flash, Response, make_response, jsonify
from helloflask.models import Patient, Doctor, Pat_Usercol, UsercolMaster, Log, Discode, DisCode_Usercol, Doc_Pat
from sqlalchemy import func
from sqlalchemy.sql import select, insert
from helloflask.init_db import db_session
from sqlalchemy.orm import joinedload

from pprint import pprint
import re, json

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
    # QQQ 삭제하기.
    session['loginUser'] = { 'userid': 1, 'name': '한도성' , 'utype' : True}
    s=session['loginUser']

    return render_template('main.html', utype=s['utype'], uname=s['name'])

@app.route('/main', methods=['POST'])
def get_collist():

    discode_list = Discode.query.all()
    col_list = UsercolMaster.query.all()
    usercol_list = UsercolMaster.query.join(Pat_Usercol, Pat_Usercol.usercol_id == UsercolMaster.id).filter(Pat_Usercol.pat_id == 1).all()
    
    data = [discode.get_json() for discode in discode_list]
    data1 = [col.get_json() for col in col_list]
    data2 = [usercol.get_json() for usercol in usercol_list]
    
    # discode는 질병코드, col는 증상코드, result는 환자에게 증상코드들이 선택되어 있을 때의 목록.
    return jsonify({'discode':data, 'col':data1, 'result':data2})

@app.route('/main/add_col/<coltype>', methods=['POST'])
def add_col(coltype):
    
    id = request.form.get('id')
    
    if coltype == 'discode_list':
        col_list = UsercolMaster.query.join(DisCode_Usercol, DisCode_Usercol.usercol_id == UsercolMaster.id).filter(DisCode_Usercol.discode_id == 311).all()

    else:
        col_list = UsercolMaster.query.filter(UsercolMaster.id == id).all()
    
    data = [col.get_json() for col in col_list]
    
    return jsonify({'result':data})

@app.route('/main/w', methods=['POST'])
def write():
    print("::::::")
    
    immutableMultiDict = request.form

    jsonData = immutableMultiDict.to_dict(flat=False)

    col_list = [jsonData[d][0] for i, d in enumerate(jsonData)]

    print(col_list)

    try:
        db_session.bulk_insert_mappings(Pat_Usercol,data_list)
        db_session.commit()  
        # custom_res = Response("Custom Response", 200, {'message': 'success'})
        custom_res = {"code" : 200, "message" : "sucess"}

    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        # custom_res = Response("Custom Response", 500, {'message': sqlerr})
        custom_res = {"code" : 500, "message" : sqlerr}
    
    return jsonify(custom_res)

    
    
    # ImmutableMultiDict([('req[]', '1'), ('req[]', '2'), ('req[]', '11'), ('req[]', '14')])

    return jsonify({'result':"OK"})

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

@app.route('/log/w', methods=['POST'])
def log_write():

    pat_id = session['loginUser']['userid']
    request_list = request.form

    pattern = re.compile("[0-9]+")

    data_list = []
    
    for i, k in enumerate(request_list):
        data = {}
        kk = re.findall(pattern,k)[0]
        data['pat_id'] = pat_id
        data['usercol_id'] = kk
        data['value'] = request_list[k]
        data_list.append(data)

    # Log table에 executemany
    try:
        db_session.bulk_insert_mappings(Log,data_list)
        db_session.commit()  
        # custom_res = Response("Custom Response", 200, {'message': 'success'})
        custom_res = {"code" : 200, "message" : "sucess"}

    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        # custom_res = Response("Custom Response", 500, {'message': sqlerr})
        custom_res = {"code" : 500, "message" : sqlerr}
    
    return jsonify(custom_res)
