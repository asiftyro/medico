from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from application.model import User
from application.form import AdminSettingsForm
from application.authentication import admin_required
from application.database import db

blueprint = Blueprint('admin_bp', __name__, url_prefix='/admin')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
  user = User.query.get(current_user.id)
  admin_form = AdminSettingsForm(obj=user)
  if admin_form.validate_on_submit():
    user.username=admin_form.username.data
    user.fullname=admin_form.fullname.data
    user.dob=admin_form.dob.data
    user.sex=admin_form.sex.data
    user.blood=admin_form.blood.data
    user.email=admin_form.email.data
    user.address=admin_form.address.data
    db.session.commit()
    flash('Settings saved successfully.', 'success')
    return redirect(url_for('admin_bp.index'))
  return render_template('admin/index.html', form=admin_form)