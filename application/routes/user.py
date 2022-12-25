from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from application.database import db
from application.model import User, Prescription
from application.form import CreateUserForm, EditUserForm, CaseAnalysisForm
from application.helper import get_unique_id, save_user_avatar_thumbnail, save_case_avatar_thumbnail
import os
import copy


blueprint = Blueprint('user_bp', __name__, url_prefix='/user')


@blueprint.route('/analysis/<username>', methods=['GET', 'POST'])
def analysis(username):
  user = User.query.filter(User.username == username).first_or_404()
  fresh_user_dict = copy.deepcopy(user.to_dict())

  prev_case_photo_1 = user.case_photo_1
  prev_case_photo_2 = user.case_photo_2
  prev_case_photo_3 = user.case_photo_3
  prev_case_photo_4 = user.case_photo_4
  user.case_photo_1 = ''
  user.case_photo_2 = ''
  user.case_photo_3 = ''
  user.case_photo_4 = ''

  case_analysis_form = CaseAnalysisForm(obj=user)

  if case_analysis_form.validate_on_submit():
    case_analysis_form.populate_obj(user)
    case_photo_1 = case_analysis_form.case_photo_1.data
    case_photo_2 = case_analysis_form.case_photo_2.data
    case_photo_3 = case_analysis_form.case_photo_3.data
    case_photo_4 = case_analysis_form.case_photo_4.data
    if case_photo_1:
      unique_case_photo_1_name = get_unique_id() + ".png"
      case_photo_1_path = os.path.join(current_app.config['CASE_PHOTO_DIR'], unique_case_photo_1_name)
      save_case_avatar_thumbnail(case_photo_1, case_photo_1_path)
      user.case_photo_1 = unique_case_photo_1_name
    else:
      user.case_photo_1 = prev_case_photo_1

    if case_photo_2:
      unique_case_photo_2_name = get_unique_id() + ".png"
      case_photo_2_path = os.path.join(current_app.config['CASE_PHOTO_DIR'], unique_case_photo_2_name)
      save_case_avatar_thumbnail(case_photo_2, case_photo_2_path)
      user.case_photo_2 = unique_case_photo_2_name
    else:
      user.case_photo_2 = prev_case_photo_2

    if case_photo_3:
      unique_case_photo_3_name = get_unique_id() + ".png"
      case_photo_3_path = os.path.join(current_app.config['CASE_PHOTO_DIR'], unique_case_photo_3_name)
      save_case_avatar_thumbnail(case_photo_3, case_photo_3_path)
      user.case_photo_3 = unique_case_photo_3_name
    else:
      user.case_photo_3 = prev_case_photo_3

    if case_photo_4:
      unique_case_photo_4_name = get_unique_id() + ".png"
      case_photo_4_path = os.path.join(current_app.config['CASE_PHOTO_DIR'], unique_case_photo_4_name)
      save_case_avatar_thumbnail(case_photo_4, case_photo_4_path)
      user.case_photo_4 = unique_case_photo_4_name
    else:
      user.case_photo_4 = prev_case_photo_4

    db.session.add(user)
    db.session.commit()
    flash('Case analysis notes updated.', 'success')
    return redirect(url_for('user_bp.treatment', username=user.username))
  elif request.method == 'POST':
    flash('Please check form fields.', 'error')
  return render_template('user/analysis.html', user=fresh_user_dict, form=case_analysis_form)


@blueprint.route('/edit/<username>', methods=['GET', 'POST'])
def edit(username):
  user = User.query.filter(User.username == username).first_or_404()
  fresh_user_dict = copy.deepcopy(user.to_dict())
  prev_avatar = user.avatar
  user.avatar = ''
  edit_user_form = EditUserForm(obj=user)
  if edit_user_form.validate_on_submit():
    edit_user_form.populate_obj(user)
    avatar = edit_user_form.avatar.data
    if avatar:
      unique_avatar_name = get_unique_id() + ".png"
      user_avatar_path = os.path.join(current_app.config['USER_AVATAR_DIR'], unique_avatar_name)
      save_user_avatar_thumbnail(avatar, user_avatar_path)
      user.avatar = unique_avatar_name
    else:
      user.avatar = prev_avatar
    db.session.add(user)
    db.session.commit()
    flash('Information updated.', 'success')
    return redirect(url_for('user_bp.view', username=user.username))
  elif request.method == 'POST':
    flash('Please check form fields.', 'error')
  return render_template('user/edit.html', form=edit_user_form, user=fresh_user_dict)


@blueprint.route('/treatment/<username>', methods=['GET'])
def treatment(username):
  user = User.query.filter(User.username == username).first_or_404()
  prescription = Prescription.query.filter((Prescription.author==5) & (Prescription.patient_id==user.id))
  return render_template('user/treatment.html', user=user.to_dict(), prescription=prescription)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
  create_user_form = CreateUserForm()
  if create_user_form.validate_on_submit():
    user = User()
    create_user_form.populate_obj(user)
    del user.avatar  # uploaded file will not be stored in db
    avatar = create_user_form.avatar.data
    if avatar:
      unique_avatar_name = get_unique_id() + ".png"
      user_avatar_path = os.path.join(current_app.config['USER_AVATAR_DIR'], unique_avatar_name)
      save_user_avatar_thumbnail(avatar, user_avatar_path)
      user.avatar = unique_avatar_name
    db.session.add(user)
    db.session.commit()
    flash('Patient information added.', 'success')
    return redirect(url_for('user_bp.view', username=create_user_form.username.data))
  elif request.method == 'POST':
    flash('Please check form fields.', 'error')

  return render_template("user/create.html", form=create_user_form)


@blueprint.route('/<username>', methods=['GET'])
def view(username):
  user = User.query.filter(User.username == username).first_or_404()
  return render_template('user/view.html', user=user.to_dict())


@blueprint.route('/', methods=['GET'])
def index():
  return render_template('user/index.html')


@blueprint.route('/api/list')
def data():
  query = User.query.filter(User.admin == 0)

  # search filter
  search = request.args.get('search')
  if search:
    query = query.filter(
        db.or_(User.username.like(f'%{search}%'), User.fullname.like(f'%{search}%'), User.dob.like(f'%{search}%')))
  total = query.count()

  # sorting
  sort = request.args.get('sort')
  if sort:
    order = []
    for s in sort.split(','):
      direction = s[0]
      name = s[1:]
      if name not in ['username', 'fullname', 'dob', 'sex', 'active']:
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
