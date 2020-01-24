import os
from flask import Flask, request, render_template, flash, redirect, jsonify, url_for, session
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import configparser
import requests


config = configparser.ConfigParser()
config.read('instance/config.ini')

platform = os.getenv('MY_ENV')
print(f'MY_ENV - {platform}')

if platform == 'development':
    devel = True
    conf = config['DEVEL']
else:
    devel = False
    conf = config['PRODUCTION']

nexmo_api_key = conf['NEXMO_API_KEY']
nexmo_api_secret = conf['NEXMO_API_SECRET']

vbc_acc = conf['VBC_ACC']

# This is for VBC QA7 Env fix.
qa7_fix_c = conf['QA7_FIX']
if qa7_fix_c.lower() == 'yes':
    qa7_fix = True
else:
    qa7_fix = False

port = int(conf['PORT'])

answer_url = conf['ANSWER_URL']
base_url = conf['BASE_URL']

google_client_id = conf['GOOGLE_CLIENT_ID']

application = app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'
bcrypt = Bcrypt()

from views import *

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=port)

