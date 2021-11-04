import os
from flask import request
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

db_config = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else 'user=postgres password=password'


def getUserPass():
    """
    @return: returns a tuple containing username and password from frontend
    """
    return request.form.get('name'), request.form.get('password')


def isUser(username):
    """
    checks if user exists
    @param username: username to be checked
    @return: True if user exists, False otherwise
    """
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users where username = %s ", (username,))
    if cur.fetchone():
        return True
    return False


def registerUser(user):
    """
    get username from frontend
    attempts to add user to database
    @return: username if user was added, False otherwise
    """
    # if not isUser(user[0]):
    if len(user[0]) > 0 and len(user[1]) > 0:  # could implement stronger password check here
        conn = psycopg2.connect(db_config, sslmode='require')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                    (user[0], generate_password_hash(user[1]),))
        conn.commit()
        return user[0]
    return False


def loginUser():
    """
    get username from frontend
    attempts to login user
    @return: username if username/password correct, False otherwise
    """
    user = getUserPass()
    if isUser(user[0]):
        conn = psycopg2.connect(db_config, sslmode='require')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users where username = %s ", (user[0],))
        password = cur.fetchone()
        if password is not None and check_password_hash(password[1], user[1]):
            return user[0]
    return False

def getNewTask():
    """
    @return: returns a tuple containing task info from frontend
    """
    return request.form.get('new_task'),request.form.get('deadline')
