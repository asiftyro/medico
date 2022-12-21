from flask import Blueprint
from application.models import User

blueprint = Blueprint('auth_bp', __name__, url_prefix='/auth')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
  return "auth"