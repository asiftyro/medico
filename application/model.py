import datetime
from dateutil.relativedelta import relativedelta
from flask import url_for, jsonify
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
# from application.routes.authentication.login_manager import login_manager
from application.database import db


class User(db.Model, UserMixin):

  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(16), unique=True, nullable=False)
  password_hash = db.Column(db.String(128))
  fullname = db.Column(db.String(64), nullable=False)
  dob = db.Column(db.Date, nullable=False)
  sex = db.Column(db.String(1), nullable=False)
  blood = db.Column(db.String(3))
  reference = db.Column(db.String(64))
  email = db.Column(db.String(64), nullable=True, unique=True)
  address = db.Column(db.String(64))
  photo = db.Column(db.String(128))
  admin = db.Column(db.SmallInteger, nullable=False, default=0)
  active = db.Column(db.SmallInteger, nullable=False, default=0)
  author = db.Column(db.Integer, db.ForeignKey("user.id"), default=1) # TODO: get from logged in user
  created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
  modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(datetime.timezone.utc))
  author_desc = db.relationship("User", remote_side=[id])

  def __repr__(self):
    return f'<User: {self.id}>'

  @property
  def password(self):
    return self.password_hash

  @password.setter
  def password(self, plaintext_password):
    self.password_hash = generate_password_hash(plaintext_password, method='sha256')

  def check_password(self, plaintext_password):
    return check_password_hash(self.password, plaintext_password)

  def get_id(self):
    return self.username

  def is_active(self):
    return self.active

  def is_admin(self):
    return self.admin

  def to_dict(self):
    avatar = ''
    if self.photo:
      avatar = url_for('static', filename=f'img/user-avatar/{self.photo}')
    elif not self.photo and self.sex == 'M':
      avatar = url_for('static', filename='img/default-avatar-male.png')
    elif not self.photo and self.sex == 'F':
      avatar = url_for('static', filename='img/default-avatar-female.png')
    else:
      avatar = url_for('static', filename='img/default-avatar-other.png')

    return {
        'id': self.id,
        'username': self.username,
        'fullname': self.fullname,
        'dob': self.dob,
        'dob_str': self.dob.strftime("%Y-%m-%d"),
        'age': "{0.years}y {0.months}m {0.days}d".format(  relativedelta(self.dob , datetime.date.today())),
        'sex': self.sex,
        'blood': self.blood,
        'reference': self.reference,
        'email': self.email,
        'address': self.address,
        'photo': avatar,
        'admin': self.admin,
        'active': self.active,
        'author': self.author,
        'created_at': self.created_at,
        'modified_at': self.modified_at,
        "author_username": self.author_desc.username,
    }


# @login_manager.user_loader
# def load_user(user_id):
#   return User.query.filter_by(username=user_id).first()
