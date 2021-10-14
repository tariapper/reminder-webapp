# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
import json
import os
import sys

import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/test')
def index2():
    db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'

    print(db_config)

    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username varchar, name varchar);")
    cur.execute("INSERT INTO users (username, name) VALUES (%s, %s)", ("hartloff", "test",))

    cur.execute("SELECT * FROM users;")
    data_from_database = cur.fetchone()
    conn.commit()

    print(data_from_database)
    return str(db_config)


@app.route('/createAccount')
def createAcc(un,p):
    db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts (username varchar, password varchar);")
    cur.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (un, p,))


@app.route('/')
def index():
    #login()
    return render_template('login.html')


@app.post("/userLogin")
def userLogin():
    content = request.get_data()
    content = content.decode()
    unpackJson(content)
    return ""

def unpackJson(jsonDict):
    return
    #Kurt will implement unpacking of json string. Keys are "username" and "password"
    #return (username,password)

if __name__=="__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host="0.0.0.0", port=port, debug=True)
    # print(flask.__version__)



#content_ = json.loads(content)
#print(content_['username'])
#print(content_['password'])
