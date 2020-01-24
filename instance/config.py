from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'sqlite:///heartplace_db.db'

SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'dsaDfdfsgr989234f@#gfdsaqzdf98sdf0a'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

# To create db tables in Python console run:

# from database import db
# from database import user, smart_numbers, google_auth
# db.create_all()
# db.session.commit()
# db.session.close()