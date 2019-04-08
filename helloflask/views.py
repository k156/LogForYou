from helloflask import app
from flask import render_template, request, session, redirect, flash
from helloflask.models import Patient, Doctor
from helloflask.init_db import db_session
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

@app.route('/test')
def test():
    return render_template("test.html")

    
@app.route('/sign_up', methods=['GET'])
def show_sign_up():
    return render_template("sign_up.html")

@app.route('/sign_up', methods=['POST'])
def sign_up():
    print("1111111111111111111111111")
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    username = request.form.get('username')

    if password != password2:
        flash("암호를 정확히 입력하세요!!")
        return render_template("sign_up.html", email=email, username=username)
    else:
        u = Patient(email, password, username, True)
        try:
            db_session.add(u)
            db_session.commit()        
            flash("%s 님, 가입을 환영합니다!" % username)
            return redirect("/sign_in")
        
        except:
            db_session.rollback()
            flash ("정보를 다시 확인해주세요.")
            return render_template("sign_up.html", email=email, username=username)


