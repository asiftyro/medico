from flask import Blueprint, render_template
from flask_login import login_required
from application.authentication import admin_required
blueprint = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')


@blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def index():
  return render_template('dashboard/index.html')