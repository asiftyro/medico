from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from application.authentication import non_admin_required
from application.model import User, Conversation, Prescription
from application.form import ConversationForm, ChangePasswordForm
from application.database import db


blueprint = Blueprint('user_home_bp', __name__, url_prefix='/user-home')

@blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
@non_admin_required
def change_password():
  user_id = current_user.id
  user = User.query.get(user_id)
  pwd_form = ChangePasswordForm()
  if pwd_form.validate_on_submit():
    user.password = pwd_form.password.data
    db.session.add(user)
    db.session.commit()
    flash("Password changed successfully", 'success')
    return redirect(url_for('user_home_bp.index'))
  elif request.method == 'POST':
    flash('Password could not be changed. Please check form fields.', 'error')
  return render_template('user_home/user_change_password.html', user=user.to_dict(), form=pwd_form)

@blueprint.route('/', methods=['GET', 'POST'])
@login_required
@non_admin_required
def index():
  user_id = current_user.id
  user = User.query.get(user_id)
  admin_id = user.author
  prescription = Prescription.query.filter(Prescription.patient_id == user_id).order_by(Prescription.created_at.desc()).limit(100).all()
  conversation = Conversation.query.filter(Conversation.patient_id == user_id).order_by(Conversation.created_at.desc()).limit(100).all()
  conv_form = ConversationForm()
  if conv_form.validate_on_submit():
    conversation_item = Conversation(conversation=conv_form.conversation.data,
                                    read=0,
                                    patient_id=user_id,
                                    admin_id=admin_id,
                                    author=user_id)
    db.session.add(conversation_item)
    db.session.commit()
    flash("Message sent.", 'success')
    return redirect(url_for('user_home_bp.index'))
  
  return render_template('user_home/index.html', user=user.to_dict(), conversation=conversation, prescription=prescription, form=conv_form)




@blueprint.route('/<username>', methods=['GET', 'POST'])
@login_required
@non_admin_required
def conversation(username):
  conv_form = ConversationForm()
  user = User.query.filter(User.username == username).first_or_404()
  author_id = current_user.id
  admin_id = current_user.id
  patient_id = user.id
  # Following query is to retrieve conversations between patients and doctor/admin
  # where patient was created by logged in doctor/admin (User.author field is the
  # creator of user)
  conversation = Conversation.query.filter((Conversation.patient_id == patient_id)
                                           & (Conversation.admin_id == admin_id)).order_by(
                                               Conversation.created_at.desc()).limit(100).all()
  if conv_form.validate_on_submit():
    conversation_item = Conversation(conversation=conv_form.conversation.data,
                                     read=0,
                                     patient_id=patient_id,
                                     admin_id=admin_id,
                                     author=author_id)
    db.session.add(conversation_item)
    db.session.commit()
    flash("Message sent.", 'success')
    return redirect(url_for('conversation_bp.conversation', username=username))
  return render_template('conversation/index.html',
                         user=user.to_dict(),
                         form=conv_form,
                         conversation=conversation)


