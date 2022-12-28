from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user


blueprint = Blueprint('index_bp', __name__, url_prefix='/')


@blueprint.route('/', methods=['GET'])
def index():
  if current_user.is_authenticated:
    if current_user.is_admin():
      return redirect(url_for('dashboard_bp.index'))
    else:
      return redirect(url_for('user_home_bp.index'))
  return render_template('index/index.html')