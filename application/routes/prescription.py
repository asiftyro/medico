import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from flask_weasyprint import HTML, render_pdf
from application.authentication import admin_required
from application.database import db
from application.model import User, Prescription
from application.form import PrescriptionCreateForm, PrescriptionEditForm, ParcelForm
from application.helper import get_unique_id, save_case_avatar_thumbnail

blueprint = Blueprint("prescription_bp", __name__, url_prefix="/prescription")

@blueprint.route("/parcel_photo_upload/<prescription_id>", methods=["POST"])
@login_required
@admin_required
def parcel_photo_upload(prescription_id):
    prescription = Prescription.query.filter(Prescription.id == prescription_id).first_or_404()
    parcel_form = ParcelForm()
    if 'save_parcel_form' in  parcel_form and parcel_form.validate_on_submit():
        parcel_photo = parcel_form.parcel_photo_1.data
        if parcel_photo:
            unique_parcel_photo_name = get_unique_id() + ".png"
            user_avatar_path = os.path.join(current_app.config["PARCEL_PHOTO_DIR"], unique_parcel_photo_name)
            save_case_avatar_thumbnail(parcel_photo, user_avatar_path)
            prescription.parcel_photo_1 = unique_parcel_photo_name
        prescription.parcel_date_1 =parcel_form.parcel_date_1.data
        db.session.add(prescription)
        db.session.commit()
        flash('Parcel photo uploaded successfullly', 'success')
        return redirect(url_for('prescription_bp.view', prescription_id=prescription.id))
    return redirect(url_for('prescription_bp.view', prescription_id=prescription.id))

@blueprint.route("/<prescription_id>", methods=["GET"])
@login_required
@admin_required
def view(prescription_id):
    """"Admin View Prescription with percel"""
    prescription = Prescription.query.filter(Prescription.id == prescription_id).first_or_404()
    user = User.query.filter(User.id == prescription.patient_id).first_or_404()
    parcel_form=ParcelForm()
    return render_template("prescription/view.html", user=user.to_dict(), prescription=prescription.to_dict(), parcel_form=parcel_form)


@blueprint.route("/create/<patient_id>", methods=["GET", "POST"])
@login_required
@admin_required
def create(patient_id):
    patient = User.query.filter(User.id == patient_id).first_or_404()
    prescription_form = PrescriptionCreateForm()
    if prescription_form.validate_on_submit():
        prescription = Prescription()
        prescription_form.populate_obj(prescription)
        prescription.patient_id = patient.id
        prescription.author = current_user.id
        db.session.add(prescription)
        db.session.commit()
        flash("Prescription created.", "success")
        return redirect(url_for("user_bp.treatment", username=patient.username))
    elif request.method == "POST":
        flash("Please check form fields.", "error")

    return render_template("prescription/create.html", user=patient.to_dict(), form=prescription_form)





@blueprint.route("/edit/<prescription_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit(prescription_id):
    prescription = Prescription.query.filter(Prescription.id == prescription_id).first_or_404()
    user = User.query.filter(User.id == prescription.patient_id).first_or_404()

    prescription_edit_form = PrescriptionEditForm(obj=prescription)
    if prescription_edit_form.validate_on_submit():
        prescription_edit_form.populate_obj(prescription)
        db.session.add(prescription)
        db.session.commit()
        flash("Prescription updated.", "success")
        return redirect(url_for("prescription_bp.view", prescription_id=prescription.id))
    elif request.method == "POST":
        flash("Please check form fields.", "error")
    return render_template(
        "prescription/edit.html", user=user.to_dict(), prescription=prescription.to_dict(), form=prescription_edit_form
    )


@blueprint.route("/print-view/<prescription_id>", methods=["GET"])
@login_required
def print_view(prescription_id):
    prescription = None
    if current_user.is_admin():
        prescription = Prescription.query.filter(
            (Prescription.id == prescription_id) & (Prescription.author == current_user.id)
        ).first_or_404()
    else:
        prescription = Prescription.query.filter(
            (Prescription.id == prescription_id) & (Prescription.patient_id == current_user.id)
        ).first_or_404()

    html = render_template("prescription/print_view.html", prescription=prescription)
    # return html
    return render_pdf(HTML(string=html))
