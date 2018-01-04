#coding:utf8

from flask import Flask, url_for


app = Flask(__name__)

app.config.from_object('sadb.config')

app.debug = True


import sadb.core
import sadb.controllers


