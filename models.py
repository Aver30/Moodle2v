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
  assessment1 = db.Column(db.String(100))
  assessment2 = db.Column(db.String(100))
  assessment3 = db.Column(db.String(100))
  groups = db.Column(db.String())
  

  def __init__(self, firstname, lastname, email, classes):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.classes = classes.lower()
    self.assessment3 = 0
    self.assessment2 = 0
    self.assessment1 = 0
    self.groups = ""

  def setAss1(self, mark ):
    self.assessment1 = mark

  def setAss2(self, mark):
    self.assessment2 = mark

  def setAss3(self, mark):
    self.assessment3 = mark

  def setgroup(self, group):
    self.groups = group

class FIT2101Rubric(db.Model):
  __tablename__ = 'fit2101rubric'
  uid = db.Column(db.Integer, primary_key = True)
  criteria= db.Column(db.String(1000))
  poor = db.Column(db.String(1000))
  satisfactory = db.Column(db.String(1000))
  good = db.Column(db.String(1000))
  totalmarks = db.Column(db.String(1000))
  assessment = db.Column(db.String(100))

  def __init__(self, criteria, poor, satisfactory, good, totalMarks, assessment): 
    self.criteria = criteria.lower()
    self.poor = poor.lower()
    self.satisfactory = satisfactory.lower()
    self.good = good.lower()
    self.totalmarks = int(totalMarks)    
    self.assessment = assessment















