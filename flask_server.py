#https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
import sys

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__=="__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host="0.0.0.0",port=port,debug=True)
    #print(flask.__version__)

