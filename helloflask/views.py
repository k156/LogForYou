from helloflask import app
from flask import render_template, request, session, redirect, flash, Response, make_response, jsonify
from helloflask.models import Patient, Doctor, Pat_Usercol, UsercolMaster, Log, Discode, DisCode_Usercol, Doc_Pat, DocPat_Disc
from sqlalchemy import func
from sqlalchemy.sql import select, insert
from helloflask.init_db import db_session
from sqlalchemy.orm import joinedload

from pprint import pprint
import re, json

from datetime import date, datetime, timedelta

def insert_data(v): 
    item = db_session.query(Table).filter_by(code = v['code']).first() 
    if item == None: 
        data = Table(v['code'], v['data']) 
        db_session.add(data) 
        db_session.commit() 



def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def login_check():
    print(">>>>", session, len(session))
    if len(session) == 0:
        print("------")
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
    
    data = {}
    data['utype'] = session['loginUser']['utype']
    return redirect('/main', res=jsonify(data))

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
        # session['next'] = '/main'
        # print(session)
        # if session.get('next'):
        #     next = session.get('next')
        #     print(">>>>>", next)
        #     del session['next']
        #     return redirect(next)
        if (utype == True):
            session['next'] = '/main'
            next = session.get('next')
            print(">>>>>", next)
            del session['next']
            return redirect(next)
        else:
            session['next'] = '/log'
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
    
    if s['utype'] == True:
        data = {}
        data['utype'] = s['utype']
        data['uname'] = s['name']
    # QQQ res로 보낸 데이터로 처리하기.
        return render_template('main.html', utype=s['utype'], uname=s['name'], res=jsonify(data))
    else:
        return redirect('/log')

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
    
    # QQQ discode 바꾸기
    if coltype == 'discode_list':
        col_list = UsercolMaster.query.join(DisCode_Usercol, DisCode_Usercol.usercol_id == UsercolMaster.id).filter(DisCode_Usercol.discode_id == 311).all()

    else:
        col_list = UsercolMaster.query.filter(UsercolMaster.id == id).all()
    
    data = [col.get_json() for col in col_list]
    
    return jsonify({'result':data})

@app.route('/main/w', methods=['POST'])
def write():
    print("::::::")
    
    isAdded = False
    doc_id = session['loginUser']['userid']
    patients_list = Doc_Pat.query.filter(Doc_Pat.pat_id == doc_id).all()
    immutableMultiDict = request.form

    jsonData = immutableMultiDict.to_dict(flat=False)
    request_data_list = [jsonData[d] for i, d in enumerate(jsonData)]
    pat_id = int(request_data_list.pop(0)[0])
    discode = int(request_data_list.pop(0)[0])
    col_list = [int(col_id) for col_id in request_data_list.pop(0)]

    # 기존 환자인지 체크
    for patient in patients_list:
        if (patient.get_json()['id'] == pat_id):
            isAdded = True
            break
        
    # 신규 환자 추가
    if(isAdded == False):
        dp = Doc_Pat(pat_id, doc_id)
        try:
            db_session.add(dp)
            db_session.commit()
        except SQLAlchemyError as sqlerr:
            db_session.rollback()
    
    # 환자의 진단된 질병코드가 있는지 확인 및 추가
    assigned_discode_list = DocPat_Disc.query.join(Doc_Pat, DocPat_Disc.docpat_id == Doc_Pat.id).filter(Doc_Pat.pat_id == pat_id).all()
    assigned_docpat = Doc_Pat.query.filter(Doc_Pat.pat_id == pat_id and Doc_Pat.doc_id == doc_id).first()
    assigned_docpat_id = assigned_docpat.get_json()['id']

    # req의 discode가 전체가 아니라, 특정한 discode가 왔고, 그 것이 등록이 안 되어 있을 때 추가
    if(discode != 0):
        assigned_discode_id_list = [assigned_discode.get_json()['discode_id'] for assigned_discode in assigned_discode_list]
        
        if(discode not in assigned_discode_id_list):
            dpd = DocPat_Disc(assigned_docpat_id, discode)
            try:
                db_session.add(dpd)
                db_session.commit()
            except SQLAlchemyError as sqlerr:
                db_session.rollback()
            
    # 리퀘스트 칼럼
    data_list = [{'pat_id': pat_id, 'usercol_id': col_id} for col_id in col_list]

    # 기존 칼럼 확인 및 새로 추가할 칼럼으로만 데이터 구성
    patuser_col_list_from_db = Pat_Usercol.query.filter(Pat_Usercol.pat_id == pat_id).all()

    patuser_col_list_from_db_min = [ col_list.get_json()['usercol_id'] for col_list in patuser_col_list_from_db]

    input_data_list = []
    if(len(patuser_col_list_from_db_min) != 0):
        for data in data_list:
            if data['usercol_id'] in patuser_col_list_from_db_min:
                patuser_col_list_from_db_min.remove(data['usercol_id'])
            else:
                input_data_list.append(data)

    delete_data_list = [{'pat_id':pat_id, 'usercol_id':col} for col in patuser_col_list_from_db_min]

    
    # 삭제할 데이터가 있으면 delete
    if (len(delete_data_list) != 0):
        
        for delete_data in delete_data_list: 
            # pu = Pat_Usercol(delete_data['pat_id'], delete_data['usercol_id'])
            delete_col = Pat_Usercol.query.filter(Pat_Usercol.pat_id == delete_data['pat_id'] , Pat_Usercol.usercol_id == delete_data['usercol_id']).first()
            delete_col_id = delete_col.get_json()['id']
            
            try:
                # db_session.delete(pu)
                Pat_Usercol.query.filter_by(id = delete_col_id).delete()
                db_session.commit()
                custom_res = {"code" : 200, "message" : "sucess"}
            # QQQ  SQLAlchemyError define 에러 해결하기.
            except:
                db_session.rollback()
                custom_res = {"code" : 500, "message" : "eerrorr"}

    # 데이터가 있으면 입력
    if len(input_data_list) != 0:
        try:
            db_session.bulk_insert_mappings(Pat_Usercol,input_data_list)
            db_session.commit()  
            custom_res = {"code" : 200, "message" : "sucess"}

        except SQLAlchemyError as sqlerr:
            db_session.rollback()
            custom_res = {"code" : 500, "message" : sqlerr}
    else:
        custom_res = {"code" : 200, "message" : "sucess"}
    
    return jsonify(custom_res)


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
    data = {}
    data['utype'] = session['loginUser']['utype']
    return render_template('sign_up.html', res=jsonify(data))

@app.route('/log')
def log():
    
    utype = session['loginUser']['utype']
    if (utype):
        return redirect('/login')
    uid = session['loginUser']["userid"]

    # petient column information
    ret = db_session.query(UsercolMaster).join(Pat_Usercol, UsercolMaster.id == Pat_Usercol.usercol_id).join(Patient, Patient.id == Pat_Usercol.doc_pat_id).filter(Patient.id == uid).all()

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

@app.route('/logs')
def logs():
    # QQQ 의사가 환자 log를 볼 때, 환자가 로그를 볼 때, 대상의 환자 id를 보내주거나 특정해놔야 한다.
    if session['loginUser']['utype'] == False:
        pat_id = session['loginUser']['userid']
    else:
        pat_id = request.form.get('pat_id')

    data = {}
    data['pat_id'] = pat_id
    return render_template('log_show.html', res=data)

@app.route('/logs/r', methods=['POST'])
def draw_table():

    pat_id = request.form.get('id')
    log_list = Log.query.filter(Log.pat_id == pat_id).all()
    log_jsonData_list = [log.get_json() for log in log_list]

    key_list = []
    for log in log_jsonData_list:
        if log['usercol_id'] not in key_list:
            key_list.append(log['usercol_id'])
    
    key_name_list = []
    boolean_col_id = []
    # QQQ Pat_Usercol의 usercol을 이용해서 각 환자의 칼럼의 이름과 아이디를 가지고 오도록 나중에 리팩!
    for key in key_list:
        col = UsercolMaster.query.filter(UsercolMaster.id == key).first()
        key_name_list.append({'key' : col.get_json()['col_name']})
        if col.get_json()['col_type'] == 3:
            boolean_col_id.append(col.get_json()['id'])

    # print("log_jsonData_list>>>>> ", log_jsonData_list)
    # sort_dic = sorted(dic.items(), key=lambda d: d[1]['name'])
    # sort_dic = sorted(log_jsonData_list, key=lambda d: d['date'])
    # print("sort_dic>>>>>>>> ", sort_dic)

    i = 0
    col2key = {}
    for jsonData in log_jsonData_list:   
        if jsonData['usercol_id'] not in col2key.keys():
            print("col2key.values()>>>>> ", col2key.keys())
            id = "col_" + str(i)
            col2key[jsonData['usercol_id']] = id
            i += 1

    data_list = []
    data = {}
    j = -1
    for jsonData in log_jsonData_list:
        p = jsonData['usercol_id']
        q = jsonData['value']
        if 'date' not in data:
            data['date'] = jsonData['date']
        else:
            # print("jsonData['date']", type(jsonData['date']), type(data['date']))
            if jsonData['date'] != data['date']:
                data_list.append(data)
                data = {}
                data['date'] = jsonData['date']

        if p in boolean_col_id:
            q = "있음" if p == True else "없음"
        data[col2key[p]] = q
            
    for data in data_list:
        data['date'] = data['date'].strftime('%Y-%m-%d')

    return jsonify({"head" : key_name_list, "body" : data_list})

    # return jsonify({"result" : "OK"})


@app.route('/logs/r2', methods=["POST","GET"])
def draw_graph():

    log_list = Log.query.filter(Log.usercol_id == 2, Log.pat_id == 1).all()

    print(">>>>>>> ", len(log_list))

    log_jsonData_list = [log.get_json() for log in log_list]

    new_jsonData_list = []
    for log_jsonData in log_jsonData_list:
        # new_jsonData = {}
        print(">>>>>>>>>>>>", type(log_jsonData['date']))
        # new_jsonData["x"] = log_jsonData['date'].timestamp() * 1000
        # new_jsonData["y"] = int(log_jsonData['value'])
        new_datalist = [log_jsonData['date'].timestamp() * 1000, int(log_jsonData['value'])]
        # new_jsonData_list.append(new_jsonData)
        new_jsonData_list.append(new_datalist)
    # new_jsonData_list.append([1551366123456, 4])
    # new_jsonData_list.append([1551366654321, 3])


    print(">>>>>>", new_jsonData_list)

    # return jsonify({"result" : "OK"})
    return jsonify({"result" : new_jsonData_list})