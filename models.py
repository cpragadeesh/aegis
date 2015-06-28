from app import db 
from werkzeug.security import generate_password_hash, check_password_hash

class Animal(db.Model):

	__tablename__ = "delta"

	id = db.Column(db.Integer, primary_key=True)
	dp = db.Column(db.String)
	name = db.Column(db.Integer)
	location = db.Column(db.String)
	species = db.Column(db.String)
	submitted = db.Column(db.String)
	points = db.Column(db.Integer)

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
		self.name = name
		self.location = location
		self.species = species
		self.dp = dp

	def __repr__(self):
		return '<%r>' % self.dp