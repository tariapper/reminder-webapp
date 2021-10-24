# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
import os
import flask
import flask_login
import util

app = flask.Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
myUser = ""


# @app.route('/test')
# def index2():
#     db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'
#
#     print(db_config)
#
#     conn = psycopg2.connect(db_config, sslmode='require')
#     cur = conn.cursor()
#     # cur.execute("DROP TABLE users;")
#     # cur.execute("CREATE TABLE users (username varchar, password varchar);")
#
#     cur.execute("SELECT * FROM users;")
#     data_from_database = cur.fetchall()
#
#     print(data_from_database)
#     return str(data_from_database)


@app.route('/', methods=['GET'])
def loginGET():
    return flask.render_template('login.html')


@app.route('/', methods=['POST'])
def loginPOST():
    username = util.loginUser()
    if username:
        user = load_user(username)
        flask_login.login_user(user, remember=True)
        return flask.redirect(flask.url_for('index_tasks_reminders'))
    return flask.redirect(flask.url_for('loginGET'))


@app.route('/register', methods=['GET'])
def registerGET():
    return flask.render_template('register.html')


@app.route('/register', methods=['POST'])
def registerPOST():
    username = util.registerUser()
    if username:
        user = load_user(username)
        flask_login.login_user(user, remember=True)
        return flask.redirect(flask.url_for('index_tasks_reminders'))
    return flask.redirect(flask.url_for('registerGET'))


@app.route('/navbar_test')
@flask_login.login_required
def navbar():
    return flask.render_template('navbar.html')


@app.route('/tasks-reminders')
@flask_login.login_required
def index_tasks_reminders():
    return flask.render_template('tasks_reminders.html', name=flask_login.current_user.username)


@app.route('/calendar')
@flask_login.login_required
def index_calendar():
    return flask.render_template('calendar.html')


@app.route('/settings')
@flask_login.login_required
def index_settings():
    return flask.render_template('settings.html')


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
    # port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    # print("test")
    app.run(host='0.0.0.0', debug=True)
