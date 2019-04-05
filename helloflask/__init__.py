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

import helloflask.views
    