from flask import Blueprint, render_template, request
from application.database import db
from application.models import User


blueprint = Blueprint('user_bp', __name__, url_prefix='/user')


@blueprint.route('/api/list')
def data():
  query = User.query

  # search filter
  search = request.args.get('search')
  if search:
    query = query.filter(db.or_(User.username.like(f'%{search}%'), User.fullname.like(f'%{search}%')))
  total = query.count()

  # sorting
  sort = request.args.get('sort')
  if sort:
    order = []
    for s in sort.split(','):
      direction = s[0]
      name = s[1:]
      if name not in ['username', 'fullname', 'sex', 'active']:
        name = 'username'
      col = getattr(User, name)
      if direction == '-':
        col = col.desc()
      order.append(col)
    if order:
      query = query.order_by(*order)

  # pagination
  start = request.args.get('start', type=int, default=-1)
  length = request.args.get('length', type=int, default=-1)
  if start != -1 and length != -1:
    query = query.offset(start).limit(length)

  # response
  return {
      'data': [user.to_dict() for user in query],
      'total': total,
  }


@blueprint.route('/', methods=['GET'])
def index():
  return render_template('user/index.html')