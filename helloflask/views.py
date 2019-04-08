from helloflask import app
from flask import render_template, request, session, redirect, flash
from helloflask.models import Patient, Doctor, Pat_Usercol, UsercolMaster
from sqlalchemy import func
from helloflask.init_db import db_session
from sqlalchemy.orm import joinedload

from datetime import date, datetime, timedelta

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

@app.route('/')
def main():
    if session.get('loginUser') == None:
        return redirect('/sign_in')
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
        return render_template("main.html", uname=session['loginUser']["name"])
        # return redirect('/')
    else:
        flash("해당 사용자가 없습니다!!")
        return render_template("form_extended.html")

@app.route('/logout')
def logout():
    if session.get('loginUser'):
        del session['loginUser']
    
    return redirect('/sign_in')

@app.route('/sign_up', methods=['GET'])
def show_sign_up():
    return render_template("sign_up_html.html")

@app.route('/sign_up', methods=['POST'])
def sign_up():
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    username = request.form.get('username')

    print(email, username)
    if password != password2:
        flash("암호를 정확히 입력하세요!!")
        return render_template("sign_up.html", email=email, username=username)
    else:
        u = Patient(email, password, username, True)
        try:
            db_session.add(u)
            db_session.commit()

        except:
            db_session.rollback()

        flash("%s 님, 가입을 환영합니다!" % username)
        return redirect("/sign_in")

@app.route('/test')
def test():
    # QQQ 가로그인 처리
    u = Patient.query.filter(Patient.email == "a@com" and Patient.password ==  func.sha2("a", 256)).first()
    # if session.get('loginUser') == None:
    #     return redirect('/sign_in')

    ret2 = db_session.query(UsercolMaster).join(Pat_Usercol, UsercolMaster.id == Pat_Usercol.usercol_id).join(Patient, Patient.id == Pat_Usercol.pat_id).filter(Patient.id == 1).all()
    


    return render_template("test.html", uname=u.name, ucol=ret2) 