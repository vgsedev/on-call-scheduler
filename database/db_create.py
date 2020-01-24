# Run it in Python console
from application import db

db.create_all()
db.session.commit()

db.session.close()

print("Tables created.")