from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from application.authentication import non_admin_required


blueprint = Blueprint('user_home_bp', __name__, url_prefix='/user-home')


@blueprint.route('/', methods=['GET'])
@login_required
@non_admin_required
def index():
  # if current_user.is_admin():
  #   return redirect(url_for('dashboard_bp.index'))
  return render_template('user_home/index.html')