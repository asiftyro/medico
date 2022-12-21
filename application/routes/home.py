from flask import Blueprint, render_template


blueprint = Blueprint('home_bp', __name__, url_prefix='')


@blueprint.route('/', methods=['GET'])
def index():
  return render_template('home/index.html')