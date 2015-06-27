from flask import Flask
from flask import render_template
from flask import request, abort, redirect, url_for, make_response
import sqlite3

app = Flask(__name__)

class User():
    def __init__(self, name, karma, post_count, posts):
        self.name = name
        self.karma = karma
        self.post_count = post_count
        self.posts = posts

class dbHandler():
    def getUser(self, username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM USERS WHERE username=?;", [username])
        return c.fetchall()

def validate_login(usr, passwd):
    if usr == "admin" and passwd == "admin":
        return True
    else:
        return False
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if(validate_login(request.form['username'], request.form['password'])):
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('username', request.form['username'])
            return resp
        else:
            return render_template('login.html', error='1')
           
    else:
        return render_template('login.html', error='0')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        username = request.cookies.get('username')
        db1 = dbHandler()
        userdata = db1.getUser(username)
        print userdata
        user = User(userdata[0][0], userdata[0][1], userdata[0][2], userdata[0][3])
        return render_template('dashboard.html', user=user)
           
if __name__ == '__main__':
    app.run(debug=True)
