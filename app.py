from flask import *
from flask.ext.wtf import form
from forms import *
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
import os
from functools import wraps
from werkzeug import secure_filename
import sqlite3

USERNAME = 'Sam'
PASSWORD = 'Sam'

UPLOAD_FOLDER = 'static/pics/'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','gif','png'])

app = Flask(__name__)
app.secret_key = "asd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# db1 = sqlite3.connect("users.db")
# c = db1.cursor()
# c.execute("SELECT * FROM USERS")


from models import *


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

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def home():
	return render_template("home.html")

def validate_login(uid, passwd):
	userlist = [('sam', 'sam'), ('john', 'john')]
	for i in userlist:
		if i[0] == uid and i[1] == passwd:
			return True

	return False		

@app.route("/login", methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if (validate_login(request.form['username'], request.form['password']) == False):
		 #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error= 'Invalid credentials'
		else:
			session['logged_in'] = True
			flash('you logged in')
			resp = make_response(redirect(url_for('upload')))
			resp.set_cookie('nick', request.form['username'])
			return resp
	
	return render_template('login.html',error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('you logged out')
	return redirect(url_for('login'))

@app.route("/upload", methods = ['GET', 'POST'])
@login_required
def upload():

	form = reg(crsf_enabled= True)
	if form.validate_on_submit():
		file = form.dp.data
		if file and allowed_file(file.filename):
			filename = secure_filename(form.dp.data.filename)
			form.dp.data.save(app.config['UPLOAD_FOLDER'] + filename)
			k = filename
			animal = Animal(dp = k,
							name = form.name.data,
							location = form.location.data,
							species = form.species.data,
							submitted = request.cookies.get('nick'),
							points = 1
							)
			db.session.add(animal)
			db.session.commit()
			return render_template("success.html")
		else:
			return render_template("reject.html")

		
	return render_template("upload.html", form = form)



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'GET':
        username = request.cookies.get('nick')
        db1 = dbHandler()
        userdata = db1.getUser(username)
        print userdata
        user = User(userdata[0][0], userdata[0][1], userdata[0][2], userdata[0][3])
        j = Animal.query.all()
        
        print j

        return render_template('dashboard.html', user=user, j=j)

@app.route('/<rollno>')
def display(rollno):
	j = User.query.filter_by(rollno=rollno).first_or_404()
	return send_from_directory(app.config['UPLOAD_FOLDER'], j.dp)

@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		term = request.form['query']
		term = term.lower()
		results = []
		j = Animal.query.all()
		for animal in j:
			if (term in ''.join(animal.name.lower().split())) or (term in ''.join(animal.species.lower().split())) or (term in animal.location.lower()):
				results.append(animal)
		print results		
		return render_template('search.html', results=results)
	
	else:
		return render_template('search.html')

if __name__ == '__main__':
	app.run(debug =True)