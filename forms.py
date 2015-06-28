from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import Required

class reg(Form):
	dp = FileField('How does his look?',validators=[Required()])
	name = StringField('What is his name?')
	location  = StringField('Where did you find him?')
	species = StringField('Species?')
	submit = SubmitField('Submit')
