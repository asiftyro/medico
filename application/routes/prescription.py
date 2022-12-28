from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from application.authentication import admin_required
from application.database import db
from application.model import User, Prescription
from application.form import PrescriptionCreateForm, PrescriptionEditForm

blueprint = Blueprint('prescription_bp', __name__, url_prefix='/prescription')


@blueprint.route('/create/<patient_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def create(patient_id):
  patient = User.query.filter(User.id == patient_id).first_or_404()
  prescription_form = PrescriptionCreateForm()
  if prescription_form.validate_on_submit():
    prescription = Prescription()
    prescription_form.populate_obj(prescription)
    prescription.patient_id = patient.id
    db.session.add(prescription)
    db.session.commit()
    flash('Prescription created.', 'success')
    return redirect(url_for('user_bp.treatment', username=patient.username))
  elif request.method == 'POST':
    flash('Please check form fields.', 'error')

  
  return render_template("prescription/create.html", user=patient.to_dict(), form=prescription_form)


@blueprint.route('/<prescription_id>', methods=['GET'])
@login_required
@admin_required
def view(prescription_id):
  prescription = Prescription.query.filter(Prescription.id == prescription_id).first_or_404()
  user = User.query.filter(User.id==prescription.patient_id).first_or_404()
  return render_template('prescription/view.html', user=user.to_dict(), prescription=prescription.to_dict())

@blueprint.route('/edit/<prescription_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(prescription_id):
  prescription = Prescription.query.filter(Prescription.id == prescription_id).first_or_404()
  user = User.query.filter(User.id==prescription.patient_id).first_or_404()

  prescription_edit_form = PrescriptionEditForm(obj=prescription)
  if prescription_edit_form.validate_on_submit():
    prescription_edit_form.populate_obj(prescription)
    db.session.add(prescription)
    db.session.commit()
    flash('Prescription updated.', 'success')
    return redirect(url_for('prescription_bp.view', prescription_id=prescription.id))
  elif request.method == 'POST':
    flash('Please check form fields.', 'error')
  return render_template('prescription/edit.html', user=user.to_dict(), prescription=prescription.to_dict(), form=prescription_edit_form)


