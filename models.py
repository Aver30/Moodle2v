from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'moodle2vusers'
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(100))
  role = db.Column(db.String(100))
  password = db.Column(db.String(100))
  classes = db.Column(db.String(100))
  unit = db.Column(db.String(100))
  uid = db.Column(db.Integer, primary_key = True)

  def __init__(self, firstname, lastname, email, role, password, classes, unit):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.role = role
    self.password = password.lower()
    self.classes = classes.lower()
    self.unit = unit.lower()
     


class FIT2101Student(db.Model):

  __tablename__ = 'fit2101students'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(100))
  classes = db.Column(db.String(100))
  

  def __init__(self, firstname, lastname, email, classes):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.classes = classes.lower()




