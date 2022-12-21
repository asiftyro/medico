import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
# from application.routes.authentication.login_manager import login_manager
from application.database import db


class User(db.Model, UserMixin):

  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, nullable=False)
  password_hash = db.Column(db.String(128))
  fullname = db.Column(db.String(64), nullable=False)
  dob = db.Column(db.Date, nullable=False)
  sex = db.Column(db.String(1), nullable=False)
  blood = db.Column(db.String(3))
  reference = db.Column(db.String(64))
  email = db.Column(db.String(64), unique=True)
  address = db.Column(db.String(128))
  photo = db.Column(db.String(128))
  admin = db.Column(db.SmallInteger, nullable=False, default=0)
  active = db.Column(db.SmallInteger, nullable=False, default=0)
  password = db.Column(db.LargeBinary, nullable=False)
  author = db.Column(db.Integer, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
  modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(datetime.timezone.utc))

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
    return {
        'id': self.id,
        'username': self.username,
        'admin': self.admin,
        'active': self.active,
        'author': self.author,
        'created': self.created,
        'modified': self.modified,
    }


# @login_manager.user_loader
# def load_user(user_id):
#   return User.query.filter_by(username=user_id).first()
