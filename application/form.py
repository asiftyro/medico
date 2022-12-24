from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, BooleanField, SubmitField
from wtforms.validators import ValidationError, Email, InputRequired, Optional, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from application.model import User


class Unique(object):

  def __init__(self, model, field_name, message='Item already exists.'):
    self.model = model
    self.field_name = field_name
    self.message = message

  def __call__(self, form, field):
    query_result = self.model.query.filter(self.field_name == field.data).first()
    if query_result:
      raise ValidationError(self.message)


class CreateUserForm(FlaskForm):
  username = StringField('Mobile (Username)',
                         validators=[
                             Unique(User, User.username, "Username/Mobile already exists."),
                             InputRequired(),
                             Length(min=4, max=16)
                         ])
  password = StringField('Password', validators=[InputRequired(), Length(min=4, max=16)])
  fullname = StringField('Full Name', validators=[InputRequired(), Length(min=4, max=64)])
  dob = DateField('Date of Birth', validators=[InputRequired()])
  sex = SelectField('Sex', choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])
  blood = SelectField('Blood Group',
                      choices=[("U", "Unknown"), ("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"), ("O+", "O+"),
                               ("O-", "O-"), ("AB+", "AB+"), ("AB-", "AB-")])
  reference = StringField("Reference", validators=[Length(max=64)])
  email = StringField('Email',
                      validators=[Email(), Optional(strip_whitespace=True),
                                  Length(max=64)],
                      filters=[lambda x: x or None])
  address = StringField("Address", validators=[Length(max=64)])
  photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png'], 'Allowed JPG or PNG Images only.')])
  active = SelectField('Active', choices=[(1, "Yes"), (0, "No")])
  admin = SelectField('Admin', choices=[(0, "No"), (1, "Yes")])
  save = SubmitField('Save')



class EditUserForm(FlaskForm):
  fullname = StringField('Full Name', validators=[InputRequired(), Length(min=4, max=64)])
  dob = DateField('Date of Birth', validators=[InputRequired()])
  sex = SelectField('Sex', choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])
  blood = SelectField('Blood Group',
                      choices=[("U", "Unknown"), ("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"), ("O+", "O+"),
                               ("O-", "O-"), ("AB+", "AB+"), ("AB-", "AB-")])
  reference = StringField("Reference", validators=[Length(max=64)])
  email = StringField('Email',
                      validators=[Email(), Optional(strip_whitespace=True),
                                  Length(max=64)],
                      filters=[lambda x: x or None])
  address = StringField("Address", validators=[Length(max=64)])
  photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png'], 'Allowed JPG or PNG Images only.')])
  active = SelectField('Active', choices=[(1, "Yes"), (0, "No")])
  admin = SelectField('Admin', choices=[(0, "No"), (1, "Yes")])
  save = SubmitField('Save')
