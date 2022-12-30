from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, TextAreaField, PasswordField, BooleanField, HiddenField
from wtforms.validators import ValidationError, Email, InputRequired, Optional, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
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

class UniqueUserOnUpdate(object):

  def __init__(self, model, field_name, user_id_field, message='Item already exists.'):
    self.model = model
    self.field_name = field_name
    self.user_id_field = user_id_field
    self.message = message

  def __call__(self, form, field):
    user_id = form[self.user_id_field].data
    query_result = self.model.query.filter(self.field_name == field.data).first()
    if query_result and (query_result.id != int(user_id.strip())):
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
  avatar = FileField('Patient\' Photo', validators=[FileAllowed(['jpg', 'png'], 'Allowed JPG or PNG Images only.')])
  active = SelectField('Active', choices=[(1, "Yes"), (0, "No")])
  # admin = SelectField('Admin', choices=[(0, "No"), (1, "Yes")])
  save = SubmitField('Save')



class EditUserForm(FlaskForm):
  id = HiddenField('user_id')
  username = StringField('Mobile (Username)',
                         validators=[
                             UniqueUserOnUpdate(User, User.username, 'id', "Username/Mobile already exists."),
                             InputRequired(),
                             Length(min=4, max=16)
                         ])
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
  avatar = FileField('Patient\'s Photo', validators=[FileAllowed(['jpg', 'png'], 'Allowed JPG or PNG Images only.')])
  active = SelectField('Active', choices=[(1, "Yes"), (0, "No")])
  # admin = SelectField('Admin', choices=[(0, "No"), (1, "Yes")])
  save = SubmitField('Save')


class CaseAnalysisForm(FlaskForm):
  analysis = TextAreaField('Case Analysis',
                           validators=[Optional(strip_whitespace=True),
                                       Length(max=2048)],
                           filters=[lambda x: x or None],
                           render_kw={'rows': 10})
  case_photo_1 = FileField('Case Photo 1', validators=[FileAllowed(['jpg', 'png'], 'Allowed JPG or PNG Images only.')])
  case_photo_2 = FileField('Case Photo 2', validators=[FileAllowed(['jpg', 'png'], 'Allowed JPG or PNG Images only.')])
  case_photo_3 = FileField('Case Photo 3', validators=[FileAllowed(['jpg', 'png'], 'Allowed JPG or PNG Images only.')])
  case_photo_4 = FileField('Case Photo 4', validators=[FileAllowed(['jpg', 'png'], 'Allowed JPG or PNG Images only.')])
  save = SubmitField('Save')


class PrescriptionCreateForm(FlaskForm):
  prescription = TextAreaField('Prescription',
                               validators=[Optional(strip_whitespace=True),
                                           Length(max=2048)],
                               filters=[lambda x: x or None],
                               render_kw={'rows': 10})
  follow_up_date = DateField('Follow up date',
                             validators=[Optional(strip_whitespace=True)],
                             filters=[lambda x: x or None])
  note = TextAreaField('Notes/Outcome/Observation',
                               validators=[Optional(strip_whitespace=True),
                                           Length(max=2048)],
                               filters=[lambda x: x or None],
                               render_kw={'rows': 10})                             
  save = SubmitField('Save')


class PrescriptionEditForm(PrescriptionCreateForm):
  pass


class LoginForm(FlaskForm):
  username = StringField('Mobile/Username', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])
  remember = BooleanField('Remember me')
  submit = SubmitField('Log In')

class ConversationForm(FlaskForm):
  conversation = StringField('Message', validators=[InputRequired(), Length(max=128)])
  submit = SubmitField('Send')


class ChangePasswordForm(FlaskForm):
  password = PasswordField('New Password', validators=[InputRequired(), Length(min=4, max=16)])
  verify_password = PasswordField('Verify new Password',validators=[EqualTo('password', message='Password must match.')])
  submit = SubmitField('Change')

class AdminSettingsForm(FlaskForm):
  id = HiddenField('user_id')
  username = StringField('Mobile (Username)',
                         validators=[
                             UniqueUserOnUpdate(User, User.username, 'id', "Username/Mobile already exists."),
                             InputRequired(),
                             Length(min=4, max=16)
                         ])
  fullname = StringField('Full Name', validators=[InputRequired(), Length(min=4, max=64)])
  dob = DateField('Date of Birth', validators=[InputRequired()])
  sex = SelectField('Sex', choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])
  blood = SelectField('Blood Group',
                      choices=[("U", "Unknown"), ("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"), ("O+", "O+"),
                               ("O-", "O-"), ("AB+", "AB+"), ("AB-", "AB-")])
  email = StringField('Email',
                      validators=[Email(), Optional(strip_whitespace=True),
                                  Length(max=64)],
                      filters=[lambda x: x or None])
  address = StringField("Address", validators=[Length(max=64)])
  save = SubmitField('Save')
