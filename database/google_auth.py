import datetime
from application import db


class GoogleAuth(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    email = db.Column(db.String(50), index=True)
    calendar = db.Column(db.String(100))
    calendar_name = db.Column(db.String(100))
    credentials = db.Column(db.PickleType())


