#coding:utf8
import os
from sadb import app

def runserver():
    port = int(os.environ.get('PORT', 3000))
    app.run(host='192.168.0.101' ,port = int(os.environ.get('PORT', 3000)))
    app.run()

if __name__ == '__main__':
    runserver()