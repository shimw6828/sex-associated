#coding:utf8

from flask import Flask, url_for
from flask_restful import Api


app = Flask(__name__)

app.config.from_object('sadb.config')



#设置api
api = Api(app)

#去掉/
app.url_map.strict_slashes = False


import sadb.core

import sadb.controllers

import sadb.ajax
import sadb.test


