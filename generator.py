import sys
import datetime
# ------------------------------------------------------------
from werkzeug.security import generate_password_hash
from application import create_app
from application.models import User
from application.configuration import DevelopmentConfiguration
from application.database import db

if (len(sys.argv) == 3 and sys.argv[1] and sys.argv[2]):
  usr_name = sys.argv[1]
  pwd_hash = generate_password_hash(sys.argv[2], method='sha256')
  
  app = create_app(DevelopmentConfiguration)
  with app.app_context():
    user = User.query.filter(User.username==usr_name).first()
    if user:
      print('\n')
      print('User Exists')
      print('\n')
      print(user.to_dict())
      print('\n')
    else:
      user = User(
        username=usr_name,
        password_hash=pwd_hash,
        fullname='Super Admin',
        dob= datetime.date(1983,12,31),
        sex='M',
        author=1,
        admin=1,
        active=1
      )
      db.session.add(user)
      db.session.commit()
else:
  print('Usage:\n$ python generate.py <username> <password>')      
# ------------------------------------------------------------
import secrets

print('\n')
print('A Random 32 byte URL-Safe tokeen:')
print(secrets.token_urlsafe(32))
print('\n')
# ------------------------------------------------------------