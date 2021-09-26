#https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

if __name__=="__main__":
    Flask.run(app,"0.0.0.0",5000,True)
    #print(flask.__version__)

