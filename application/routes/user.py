from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from application.database import db
from application.model import User
from application.form import CreateUserForm
from application.helper import get_unique_id, save_user_avatar_thumbnail
import os

blueprint = Blueprint('user_bp', __name__, url_prefix='/user')


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
  create_user_form = CreateUserForm()
  if create_user_form.validate_on_submit():
    user = User()
    create_user_form.populate_obj(user)
    del user.photo # uploaded file will not be stored in db
    photo = create_user_form.photo.data
    if photo:
      unique_photo_name = get_unique_id()+".png"
      user_avatar_path = os.path.join( current_app.config['USER_AVATAR_DIR'], unique_photo_name)
      save_user_avatar_thumbnail(photo, user_avatar_path)
      user.photo = unique_photo_name
    db.session.add(user)
    db.session.commit()
    flash('Patient information added.', 'success')
    return redirect(url_for('user_bp.view', username=create_user_form.username.data))
  elif request.method=='POST':
    flash('Please check form fields.', 'error')

  return render_template("user/create.html", form=create_user_form)


@blueprint.route('/<username>', methods=['GET'])
def view(username):
  query = User.query.filter(User.username == username).first_or_404()
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
