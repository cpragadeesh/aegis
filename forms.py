from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import Required

class reg(Form):
#	rollno = StringField('Roll Number', validators=[Required()])
#	name   = StringField('Name', validators=[Required()])
#	password = PasswordField('Password',validators=[Required()])
	dp = FileField('Picture',validators=[Required()])
	submit = SubmitField('Submit')

