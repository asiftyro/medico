import functools
from flask import redirect, url_for, flash, abort
from flask_login import LoginManager, current_user
from application.model import User


login_manager = LoginManager()

# login_manager.login_view = 'auth_bp.login'
# login_manager.login_message = 'Please Login to view this page.'
# login_manager.login_message_category = 'warning'
login_success_view_admin = 'dashboard_bp.index'
login_success_view_non_admin = 'user_home_bp.index'
logout_success_view = 'auth_bp.login'
# register_success_view = 'home_bp.index'


@login_manager.user_loader
def load_user(user_id):
  if user_id is not None:
    return User.query.filter(User.username == user_id).first()
  return None


@login_manager.unauthorized_handler
def unauthorized():
  flash('You must be logged in to view that page.')
  return redirect(url_for('auth_bp.login'))


def admin_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if not current_user.is_admin():
      abort(403)
    return view(**kwargs)
  return wrapped_view

def non_admin_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if current_user.is_admin():
      abort(403)
    return view(**kwargs)
  return wrapped_view  
