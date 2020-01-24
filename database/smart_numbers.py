import datetime

from application import db


class SmartNumber(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    smart_number = db.Column(db.String(11), nullable=False)
    destination_extension = db.Column(db.String(11), nullable=False)
    nx_app_id = db.Column(db.String(100))
    google_id = db.Column(db.Integer, db.ForeignKey('google_auth.id'))


