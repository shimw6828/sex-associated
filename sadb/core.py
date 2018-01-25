from flask_pymongo import PyMongo

from sadb import app

mongo = PyMongo(app)

'''
class human(db.Model):
    __tablename__ =""
'''