from flask import *
from flask.ext.wtf import form
from forms import *
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
import os
from werkzeug import secure_filename
import uuid

UPLOAD_FOLDER = 'pics/'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','gif','png'])

app = Flask(__name__)
app.secret_key = "asd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 0.5 * 1024 * 1024

from models import *


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():

	form = reg(crsf_enabled= True)
	if form.validate_on_submit():
		file = form.dp.data
		if file and allowed_file(file.filename):
			filename = secure_filename(form.dp.data.filename)
			form.dp.data.save(app.config['UPLOAD_FOLDER'] + filename)
			k = filename
			animal = Animal(dp = k)
			db.session.add(animal)
			db.session.commit()
			return render_template("success.html")
		else:
			return render_template("reject.html")

		
	return render_template("register.html", form = form)

@app.route('/<rollno>')
def display(rollno):
	j = User.query.filter_by(rollno=rollno).first_or_404()
	return send_from_directory(app.config['UPLOAD_FOLDER'], j.dp)

if __name__ == '__main__':
	app.run(debug =True)