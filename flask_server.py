# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
import bcrypt
import json
import os
import sys

import flask
import psycopg2
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
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
    #changey

@app.post("/userLogin")
def userLogin():
    content = request.get_data()
    content = content.decode()
    up = unpackJson(content)

    db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()

    x = cur.execute("SELECT* FROM users where username = %s ", (up[0],))
    if x is not None:
        if check_password_hash(x[1], up[1]):
            flask.redirect("tasks_reminders")


@app.post("/userRegister")
def userRegister():
    content = request.get_data()
    content = content.decode()
    up = unpackJson(content)

    db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()

    x = cur.execute("SELECT COUNT(*) FROM users where username = %s ", (up[0],))
    if x == 0:
        cur.execute("INSERT INTO users (username, name) VALUES (%s, %s)", (up[0], generate_password_hash(up[1]),))
        return True
    conn.commit()
    return False


def unpackJson(jsonDict):
    ##
    username_key, password_key = 'username', 'password'
    obj = json.loads(jsonDict)
    username, password = obj[username_key], obj[password_key]
    print(username)
    print(password)
    return username, password

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/navbar_test')
def navbar():
    return render_template('navbar.html')

@app.route('/tasks-reminders')
def index_tasks_reminders():
    return render_template('tasks_reminders.html')

@app.route('/calendar')
def index_calendar():
    return render_template('calendar.html')

@app.route('/settings')
def index_settings():
    return render_template('settings.html')


if __name__=="__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host="0.0.0.0",port=port,debug=True)
    #print(flask.__version__)