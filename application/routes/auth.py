from flask import Blueprint


blueprint = Blueprint('auth_bp', __name__, url_prefix='/auth')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
  return "auth"