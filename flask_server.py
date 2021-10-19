# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
import os
import sys
import flask
import flask_login

import psycopg2
from flask import Flask, render_template, request
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
myUser = ""


@app.route('/', methods=['GET'])
def loginGET():
    return render_template('login.html')


@app.route('/', methods=['POST'])
def login():
    up = (request.form.get('name'), request.form.get('password'))

    db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users where username = %s ", (up[0],))
    x = cur.fetchone()
    if x is not None:
        if check_password_hash(x[1], up[1]):
            global myUser
            myUser = up[0]
            user = load_user(myUser)
            flask_login.login_user(user, remember=True)
            return flask.redirect(flask.url_for('index_tasks_reminders'))

    return render_template('login.html')


@app.route('/register', methods=['GET'])
def registerGET():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    up = (request.form.get('name'), request.form.get('password'))

    db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users where username = %s ", (up[0],))
    x = cur.fetchall()

    if len(x) == 0:
        cur.execute("INSERT INTO users (username, name) VALUES (%s, %s)", (up[0], generate_password_hash(up[1]),))
        conn.commit()
        global myUser
        myUser = up[0]
        user = load_user(myUser)
        flask_login.login_user(user, remember=True)
        return flask.redirect(flask.url_for('index_tasks_reminders'))
    return render_template('register.html')


@app.route('/navbar_test')
@login_required
def navbar():
    return render_template('navbar.html')


@app.route('/tasks-reminders')
@login_required
def index_tasks_reminders():
    return render_template('tasks_reminders.html', name=myUser)


@app.route('/calendar')
@login_required
def index_calendar():
    return render_template('calendar.html')


@app.route('/settings')
@login_required
def index_settings():
    return render_template('settings.html')


class User(flask_login.UserMixin):
    def __init__(self, username, active=True):
        self.username = username
        self.active = active

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


@login_manager.user_loader
def load_user(username):
    # 1. Fetch against the database a user by `id`
    # 2. Create a new object of `User` class and return it.
    return User(username, True)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host="0.0.0.0", port=port, debug=True)
