from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import logout_user, login_user, current_user
from application.authentication import load_user, login_success_view_admin, login_success_view_non_admin, logout_success_view
from application.model import User
from application.form import LoginForm


blueprint = Blueprint('auth_bp', __name__, url_prefix='/auth')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    if current_user.is_admin():
      return redirect(url_for(login_success_view_admin))
    else:
      return redirect(url_for(login_success_view_non_admin))

  login_form = LoginForm()
  if login_form.validate_on_submit():
    user = load_user(login_form.username.data)
    if user is None:
      flash('Please check your login details and try again (1).', 'error')
    elif not user.check_password(login_form.password.data):
      flash('Please check your login details and try again (2).', 'error')
    elif not user.is_active():
      flash('Your account is inactive. Please contact Administrator (3).', 'error')
    else:
      login_user(user, remember=login_form.remember.data)
      flash('Logged In successfully.', 'success')
      if user.is_admin():
        return redirect(url_for(login_success_view_admin))
      else:
        return redirect(url_for(login_success_view_non_admin))
  return render_template('auth/login.html', form=login_form)


@blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
  logout_user()
  flash('Logged out successfully.', 'info')
  return redirect(url_for(logout_success_view))