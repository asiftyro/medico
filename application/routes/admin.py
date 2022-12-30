from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user


blueprint = Blueprint('admin_bp', __name__, url_prefix='/admin')


@blueprint.route('/', methods=['GET'])
def index():
  return render_template('admin/index.html')