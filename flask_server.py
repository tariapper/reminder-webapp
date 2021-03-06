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


# @app.route('/test')
# def index2():
#     db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'
#
#     print(db_config)
#
#     import psycopg2
#     conn = psycopg2.connect(db_config, sslmode='require')
#     cur = conn.cursor()
#
#     cur.execute("SELECT * FROM tasks;")
#     data_from_database = cur.fetchall()
#
#     print(data_from_database)
#     return str(data_from_database)


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


# add code to display all tasks + form to add new task
@app.route('/', methods=['GET'])
@flask_login.login_required
def index_tasks_remindersGET():
    return flask.render_template('tasks_reminders.html', tasks=util.getTasks(flask_login.current_user.username))


# once user posts (the form), get all info and add task to database, plus update view to include this new task
@app.route('/', methods=['POST'])
@flask_login.login_required
def index_tasks_remindersPOST():
    taskInfo = util.getNewTask()
    if taskInfo[0] != '' and taskInfo[1] != '':
        util.addTask(taskInfo[0], taskInfo[1], flask_login.current_user.username)
    return flask.redirect(flask.url_for('index_tasks_remindersGET'))


@app.route('/removed', methods=['POST'])
@flask_login.login_required
def index_removed_POST():
    print(flask.request.form.get("myTask"))
    util.removeTask(flask.request.form.get("myTask"))
    return flask.redirect(flask.url_for('index_tasks_remindersGET'))


@app.route('/calendar', methods=['POST'])
def index_calendarPOST():
    import json
    a = flask.request.data
    temp = json.loads(a)
    bruh = temp['bruh']
    if bruh == 1:
        util.addTask(temp['title'], temp['start'], flask_login.current_user.username)
    elif bruh == 2:
        pass 

    return flask.redirect('/calendar')

@app.route('/calendar')
@flask_login.login_required
def index_calendar():
    tmplt = "{title: '%s', start: '%s', allDay: true, id: '%s'}"
    e = util.getTasks(flask_login.current_user.username)
    s = '['

    # task is a tuple in the form of (id, username, task, ddl)
    for i in e:
        s += tmplt % (i[2], str(i[3]), i[2]) + ','

    s += ']'

    return flask.render_template('calendar.html', event = s)


@app.route('/settings',  methods=['GET'])
@flask_login.login_required
def settings_GET():
    return flask.render_template('settings.html')


@app.route('/settings', methods=['POST'])
@flask_login.login_required
def settings_POST():
    util.changePassword(flask_login.current_user.username)
    return flask.render_template('settings.html')

@app.route('/removeAll', methods=['POST'])
@flask_login.login_required
def index_removedAll_POST():
    util.removeAllTasks(flask_login.current_user.username)
    return flask.redirect(flask.url_for('index_tasks_remindersGET'))

@app.route('/reset', methods=['POST'])
@flask_login.login_required
def reset_POST():
    util.deleteAccount(flask_login.current_user.username)
    util.removeAllTasks(flask_login.current_user.username)
    return flask.redirect(flask.url_for('registerGET'))



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
