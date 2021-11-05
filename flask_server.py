# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
import os
import sys
import flask
import flask_login
import util

app = flask.Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
login_manager = flask_login.LoginManager()
login_manager.login_view = 'loginGET'
login_manager.init_app(app)


@app.route('/test')
def index2():
    db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'

    print(db_config)

    import psycopg2
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users;")
    data_from_database = cur.fetchall()

    print(data_from_database)
    return str(data_from_database)


@app.route('/login', methods=['GET'])
def loginGET():
    return flask.render_template('login.html')


@app.route('/login', methods=['POST'])
def loginPOST():
    username = util.loginUser()
    if not username:
        flask.flash('Username/password incorrect.')
        return flask.redirect(flask.url_for('loginGET'))

    user = load_user(username)
    flask_login.login_user(user, remember=True)
    return flask.redirect(flask.url_for('index_tasks_remindersGET'))


@app.route('/register', methods=['GET'])
def registerGET():
    return flask.render_template('register.html')


@app.route('/register', methods=['POST'])
def registerPOST():
    user = util.getUserPass()
    if util.isUser(user[0]):
        flask.flash('User already exists.')
        return flask.redirect(flask.url_for('registerGET'))

    username = util.registerUser(user)
    if not username:
        flask.flash('Username/password cannot be empty.')
        return flask.redirect(flask.url_for('registerGET'))

    user = load_user(username)
    flask_login.login_user(user, remember=True)
    return flask.redirect(flask.url_for('index_tasks_remindersGET'))


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('loginGET'))


@app.route('/navbar_test')
@flask_login.login_required
def navbar():
    return flask.render_template('navbar.html')


#add code to display all tasks + form to add new task
@app.route('/', methods=['GET'])
@flask_login.login_required
def index_tasks_remindersGET():
    #call database function to get all tasks
    #name=flask_login.current_user.username
    tasks = [("testfkjhfkjdsfhdskjfhdskjhfdskjfhdskjfhdfkjdshdkjhfsjdhdksjfhdkjlfhdkjshfkjdshftestfkjhfkjdsfhdskjfhdskjhfdskjfhdskjfhdfkjdshdkjhfsjdhdksjfhdkjlfhdkjshfkjdshftestfkjhfkjdsfhdskjfhdskjhfdskjfhdskjfhdfkjdshdkjhfsjdhdksjfhdkjlfhdkjshfkjdshftestfkjhfkjdsfhdskjfhdskjhfdskjfhdskjfhdfkjdshdkjhfsjdhdksjfhdkjlfhdkjshfkjdshftestfkjhfkjdsfhdskjfhdskjhfdskjfhdskjfhdfkjdshdkjhfsjdhdksjfhdkjlfhdkjshfkjdshf", "1234"), ("tesst", "234")]
    return flask.render_template('tasks_reminders.html', tasks=tasks)

#once user posts (the form), get all info and add task to database, plus update view to include this new task
@app.route('/', methods=['POST'])
@flask_login.login_required
def index_tasks_remindersPOST():
    taskInfo = util.getNewTask()
    print(taskInfo)
    #util.addTask(taskInfo[0],taskInfo[1],flask_login.current_user.username)
    return flask.redirect(flask.url_for('index_tasks_remindersGET'))


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
    return User(username, True)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host='0.0.0.0', port=port, debug=True)
