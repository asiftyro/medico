from flask import Blueprint, render_template, request
from application.database import db
from application.model import User


blueprint = Blueprint('user_bp', __name__, url_prefix='/user')


@blueprint.route('/<username>', methods=['GET'])
def view(username):
  query = User.query.filter(User.username == username).first_or_404();
  return render_template('user/view.html', user=query.to_dict())

@blueprint.route('/', methods=['GET'])
def index():
  return render_template('user/index.html')


@blueprint.route('/api/list')
def data():
  query = User.query.filter(User.admin == 0)

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
