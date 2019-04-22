from flask import Flask, g, Response, make_response, request, render_template, Markup, session, redirect, flash
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from helloflask.init_db import init_database, db_session
from helloflask.models import Patient, Doctor, Log, UsercolMaster, Pat_Usercol
from flask import url_for
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from keys import secret_key



app = Flask(__name__)
app.debug = True  

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

app.config.update(
	SECRET_KEY=secret_key,
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

import helloflask.views
    