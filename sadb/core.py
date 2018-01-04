from flask_sqlalchemy import SQLAlchemy

from sadb import app

db = SQLAlchemy(app)

'''
class human(db.Model):
    __tablename__ =""
'''