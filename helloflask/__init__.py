from flask import Flask, g, Response, make_response, request, render_template, Markup
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from helloflask.templates.init_db import init_database, db_session


app = Flask(__name__)
app.debug = True  


@app.route('/res1')