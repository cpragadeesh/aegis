from app import db 
from werkzeug.security import generate_password_hash, check_password_hash

class Animal(db.Model):

	__tablename__ = "delta"

	id = db.Column(db.Integer, primary_key=True)
#	rollno = db.Column(db.Integer, unique=True, nullable=False)
#	name = db.Column(db.String, nullable=False)
#	password = db.Column(db.String, nullable= False)
	dp = db.Column(db.String, nullable= False)

#	@property
#	def password(self):
#		raise AttributeError('password in not a readable attribute')

#	@password.setter
#	def password(self, password):
#		self.password_hash = generate_password_hash(password)
#
#	def verify_password(self,password):
#		return check_password_hash(self.password_hash, password)

	def __int__(self,dp):
#		self.rollno = rollno
#		self.name = name
#		self.password = password
		self.dp = dp

	def __repr__(self):
		return '<%r>' % self.dp
