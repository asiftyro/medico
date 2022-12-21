from flask import Blueprint


blueprint = Blueprint('user_bp', __name__, url_prefix='/user')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
  return "user"