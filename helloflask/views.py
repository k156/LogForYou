from helloflask import app
from flask import render_template, request, session, redirect, flash, Response, make_response, jsonify
from helloflask.models import Patient, Doctor, Pat_Usercol, UsercolMaster, Log, Discode, DisCode_Usercol
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
        session['loginUser'] = { 'userid': u.id, 'name': u.name }
        if session.get('next'):
            next = session.get('next')
            del session['next']
            return redirect(next)
    else:
        flash("해당 사용자가 없습니다!!")
        return redirect("/login")

    return render_template('main.html', utype=utype, uname=session['loginUser']['name'])

@app.route('/logout')
def logout():
    print("444444444")
    if session.get('loginUser'):
        del session['loginUser']
    
    return redirect('/login')

@app.route('/main')
def main():
    print("55555555")
    return render_template('main.html')

@app.route('/main/s', methods=['POST'])
def search():
    print("6666666666")
    pat_id = request.form.get('s')
    
    p = Patient.query.filter(Patient.id == pat_id).first()

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

<<<<<<< HEAD


@app.route('/log/write', methods=['POST'])
def write_log():

    pat_id = session['loginUser']['userid']
    request_list = request.form
    lst = []

    for req in request_list:
        data = request.form.get(req)
        l = Log(pat_id, req, data)
        lst.append(l.get_json())
    # Log table에 executemany
    try:
        db_session.bulk_insert_mappings(Log,lst)
        db_session.commit()
        custom_res = Response("Custom Response", 200, {'message': 'success'})

    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        custom_res = Response("Custom Response", 500, {'message': sqlerr})
    
    return make_response(custom_res)


@app.route('/register')
def register():
    dc_list = Discode.query.all()

    usercol_list = UsercolMaster.query.all()

    print("=====================")
    for dc in dc_list:
        print(dc.get_json())
        

    return render_template('search.html', ret=dc_list, ret1=usercol_list)


@app.route('/test', methods=['POST'])
def test_post():
    
    discode = request.form.get('discode')
    discode = '311' # QQQ 나중에 db 완성되면 지우기

    column_list = db_session.query(UsercolMaster).join(DisCode_Usercol, UsercolMaster.id == DisCode_Usercol.usercol_id).filter(DisCode_Usercol.discode_id == discode).all()
    
    result = {}

    result['rs'] = []

    for cl in column_list:
        result['rs'].append(cl.get_json())

    return jsonify(result)

@app.route('/patient/search', methods=['POST'])
def search_patient():
    pat_id = request.form.get('pat_id')

    p = Patient.query.filter(Patient.id == pat_id).first()
    r = p.name

    return  render_template('search.html', result=r)

@app.route('/discode', methods=['POST'])
def get_discode():
    dc_list = Discode.query.all()

    data = {}

    data['type'] = 1
    data['result'] = []
    
    for dc in dc_list:
        small_data = dc.get_json()
        small_data['name'] = dc.get_json()['disease']
        data['result'].append(small_data)

    print(data)

    return jsonify(data)
    


@app.route("/test_input", methods=['POST'])
def column_input():
    
    request_list = request.form
    lst = []
    pat_id = 1  # QQQQQ 지우기

    for req in request_list.values():
        p = Pat_Usercol(pat_id, req)
        lst.append(p.get_json())
    
    try:
        db_session.bulk_insert_mappings(Pat_Usercol,lst)
        db_session.commit()
        custom_res = jsonify({'message': 'success'})

    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        print("Error", sqlerr)
        custom_res = jsonify({'message': sqlerr})

    return make_response(custom_res)
=======
>>>>>>> master
