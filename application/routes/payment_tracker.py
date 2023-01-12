import re
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from application.authentication import admin_required
from application.database import db
from application.model import PaymentTracker, User, PaymentDescription, PaymentMethod
from application.form import (
    PaymentInstructionCreateForm,
    PaymentInstructionEditForm,
    PaymentDescriptionCreateForm,
    PaymentMethodCreateForm,
)
from application.helper import string_date_as_timezone


blueprint = Blueprint("payment_tracker_bp", __name__, url_prefix="/payment-tracker")


@blueprint.route("/delete-method-parameter/<id>", methods=["POST"])
@login_required
@admin_required
def delete_method_parameter(id):
    obj = PaymentMethod.query.filter(PaymentMethod.id == id).one()

    db.session.delete(obj)
    db.session.commit()

    flash(f"Payment method '{obj.payment_method}' deleted successfully.", "success")
    return redirect(url_for("payment_tracker_bp.parameter"))


@blueprint.route("/delete-description-parameter/<id>", methods=["POST"])
@login_required
@admin_required
def delete_description_parameter(id):
    obj = PaymentDescription.query.filter(PaymentDescription.id == id).one()

    db.session.delete(obj)
    db.session.commit()

    flash(f"Payment description '{obj.payment_description}' deleted successfully.", "success")
    return redirect(url_for("payment_tracker_bp.parameter"))


@blueprint.route("/parameter", methods=["GET", "POST"])
@login_required
@admin_required
def parameter():
    payment_description_form = PaymentDescriptionCreateForm()
    payment_method_form = PaymentMethodCreateForm()
    payment_description = PaymentDescription.query.all()
    payment_method = PaymentMethod.query.all()

    if "save_payment_method" in request.form and payment_method_form.validate_on_submit():
        PayMethod = PaymentMethod()
        payment_method_form.populate_obj(PayMethod)
        PayMethod.author = current_user.id
        db.session.add(PayMethod)
        db.session.commit()
        flash("New payment method added successfully.", "success")
        return redirect(url_for("payment_tracker_bp.parameter"))

    if "save_payment_description" in request.form and payment_description_form.validate_on_submit():
        PayDesc = PaymentDescription()
        payment_description_form.populate_obj(PayDesc)
        PayDesc.author = current_user.id
        db.session.add(PayDesc)
        db.session.commit()
        flash("New payment description added successfully.", "success")
        return redirect(url_for("payment_tracker_bp.parameter"))

    return render_template(
        "payment_tracker/parameter.html",
        payment_description_model=PaymentDescription,
        payment_description=payment_description,
        payment_method_model=PaymentMethod,
        payment_method=payment_method,
        payment_description_form=payment_description_form,
        payment_method_form=payment_method_form,
    )


@blueprint.route("/edit/<id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit(id):
    PayTrack = PaymentTracker.query.filter(PaymentTracker.id == id).one()
    edit_form = PaymentInstructionEditForm(obj=PayTrack)

    if "save_edited_payment_status" in request.form and edit_form.validate_on_submit():
        edit_form.populate_obj(PayTrack)
        if edit_form.payment_status.data == "1":
            PayTrack.paid_at = datetime.datetime.now(datetime.timezone.utc)
        else:
            PayTrack.paid_at = None

        PayTrack.author = current_user.id

        db.session.add(PayTrack)
        db.session.commit()

        flash("Edited successfully.", "success")
        return redirect(url_for("payment_tracker_bp.edit", id=id))
    return render_template("payment_tracker/edit.html", payment_instr_edit_form=edit_form, paym_instr=PayTrack)


@blueprint.route("/change-patient-notification/<id>", methods=["GET", "POST"])
@login_required
@admin_required
def change_patient_notification(id):
    obj = PaymentTracker.query.filter(PaymentTracker.id == id).one()
    obj.author = current_user.id
    obj.visible_to_patient = not obj.visible_to_patient

    db.session.add(obj)
    db.session.commit()

    sts = ["Unnotified", "Notified"]
    flash(f"Payment Instruction #{id} {sts[obj.visible_to_patient]} to patient successfully.", "success")
    if request.form["return_url"]:
        return redirect(request.form["return_url"])
    else:
        return redirect(url_for("payment_tracker_bp.instructions"))


@blueprint.route("/change-payment-status/<id>", methods=["GET", "POST"])
@login_required
@admin_required
def change_payment_status(id):
    obj = PaymentTracker.query.filter(PaymentTracker.id == id).one()
    obj.author = current_user.id
    obj.payment_status = not obj.payment_status
    if obj.payment_status:
        obj.paid_at = datetime.datetime.now(datetime.timezone.utc)
    else:
        obj.paid_at = None

    db.session.add(obj)
    db.session.commit()

    sts = ["Unpaid", "Paid"]
    flash(f"Payment Instruction #{id} status changed to {sts[obj.payment_status]} successfully.", "success")
    if request.form["return_url"]:
        return redirect(request.form["return_url"])
    else:
        return redirect(url_for("payment_tracker_bp.instructions"))


@blueprint.route("/delete/<id>", methods=["POST"])
@login_required
@admin_required
def delete(id):
    obj = PaymentTracker.query.filter(PaymentTracker.id == id).one()

    db.session.delete(obj)
    db.session.commit()

    flash(f"Payment Instruction #{id} deleted successfully.", "success")
    if request.form["return_url"]:
        return redirect(request.form["return_url"])
    else:
        return redirect(url_for("payment_tracker_bp.instructions"))


@blueprint.route("/instructions", methods=["GET", "POST"])
@login_required
@admin_required
def instructions():
    user_id = current_user.id
    # Pagination arg
    page = request.args.get("page", 1, type=int)
    # Search args/query strings
    id = request.args.get("id", "", type=str).strip()
    patient_id = request.args.get("patient_id", "", type=str).strip()
    payment_description = request.args.get("payment_description", "", type=str).strip()
    payment_status = request.args.get("payment_status", "", type=str).strip()
    payment_method = request.args.get("payment_method", "", type=str).strip()
    visible_to_patient = request.args.get("visible_to_patient", "", type=str).strip()
    created_at_start = request.args.get("created_at_start", "", type=str).strip()
    created_at_end = request.args.get("created_at_end", "", type=str).strip()
    paid_at_start = request.args.get("paid_at_start", "", type=str).strip()
    paid_at_end = request.args.get("paid_at_end", "", type=str).strip()
    # Filter/Search form is submitted
    if "submit_filter" in request.form and request.method == "POST":
        id = request.form["id"] if request.form["id"] else id
        patient_id = request.form["patient_id"] if request.form["patient_id"] else patient_id
        payment_description = (
            request.form["payment_description"] if request.form["payment_description"] else payment_description
        )
        payment_status = request.form["payment_status"] if request.form["payment_status"] else payment_status
        created_at_start = request.form["created_at_start"] if request.form["created_at_start"] else created_at_start
        created_at_end = request.form["created_at_end"] if request.form["created_at_end"] else created_at_end
        paid_at_start = request.form["paid_at_start"] if request.form["paid_at_start"] else paid_at_start
        paid_at_end = request.form["paid_at_end"] if request.form["paid_at_end"] else paid_at_end
        payment_method = request.form["payment_method"] if request.form["payment_method"] else payment_method
        visible_to_patient = (
            request.form["visible_to_patient"] if request.form["visible_to_patient"] else visible_to_patient
        )

        # Build filter query string of page url
        url_query = f"?id={id}&patient_id={patient_id}&payment_description={payment_description}&payment_status={payment_status}&created_at_start={created_at_start}&created_at_end={created_at_end}&paid_at_start={paid_at_start}&paid_at_end={paid_at_end}&payment_method={payment_method}&visible_to_patient={visible_to_patient}"
        # Redirect to built url
        return redirect(url_for("payment_tracker_bp.instructions") + url_query)

    # Time zone convertion for filter/query args with date
    if created_at_start:
        created_at_start_tz = string_date_as_timezone(created_at_start, "%Y-%m-%d", "UTC")
    if created_at_end:
        created_at_end_tz = string_date_as_timezone(created_at_end, "%Y-%m-%d", "UTC")
    if paid_at_start:
        paid_at_start_tz = string_date_as_timezone(paid_at_start, "%Y-%m-%d", "UTC")
    if paid_at_end:
        paid_at_end_tz = string_date_as_timezone(paid_at_end, "%Y-%m-%d", "UTC")

    # Build SQLAlchemy query with filter arguments
    search_queries = []
    if id:
        search_queries.append((PaymentTracker.id == id))
    if patient_id:
        search_queries.append((PaymentTracker.patient_id == patient_id))
    if payment_status:
        search_queries.append((PaymentTracker.payment_status == payment_status))
    if payment_description:
        search_queries.append((PaymentTracker.payment_description == payment_description))
    if payment_method:
        search_queries.append((PaymentTracker.payment_method == payment_method))
    if visible_to_patient:
        search_queries.append((PaymentTracker.visible_to_patient == visible_to_patient))

    if created_at_start and created_at_end:
        search_queries.append(
            (PaymentTracker.created_at >= created_at_start_tz) & (PaymentTracker.created_at <= created_at_end_tz)
        )
    elif created_at_start:
        search_queries.append((PaymentTracker.created_at == created_at_start_tz))
    elif created_at_end:
        search_queries.append((PaymentTracker.created_at == created_at_end_tz))

    if paid_at_start and paid_at_end:
        search_queries.append((PaymentTracker.paid_at >= paid_at_start_tz) & (PaymentTracker.paid_at <= paid_at_end_tz))
    elif paid_at_start:
        search_queries.append((PaymentTracker.paid_at == paid_at_start_tz))
    elif paid_at_end:
        search_queries.append((PaymentTracker.paid_at == paid_at_end_tz))

    search_query = PaymentTracker.author == user_id

    for sq in search_queries:
        search_query = search_query & sq

    # Get Payment Instructions
    payment_instr = db.paginate(
        db.select(PaymentTracker).where(search_query).order_by(PaymentTracker.id.desc()), page=page, per_page=30
    )

    # Get patient database
    patients = User.query.filter(User.author == user_id).order_by(User.fullname).all()

    # Get payment methods
    payment_methods = PaymentMethod.query.filter(PaymentMethod.author == user_id).all()

    # Get payment methods
    payment_descriptions = PaymentDescription.query.filter(PaymentDescription.author == user_id).all()

    # Remove 'page' argument if exists
    query_string = request.query_string.decode("utf-8")
    query_string = re.sub("&?page=[0-9]*", "", query_string)
    return_url = url_for("payment_tracker_bp.instructions") + "?" + query_string

    return render_template(
        "payment_tracker/index.html",
        return_url=return_url,
        payment_instr=payment_instr,
        patients=patients,
        payment_methods=payment_methods,
        payment_descriptions=payment_descriptions,
        id=id,
        patient_id=patient_id,
        payment_description=payment_description,
        payment_status=payment_status,
        created_at_start=created_at_start,
        created_at_end=created_at_end,
        paid_at_start=paid_at_start,
        paid_at_end=paid_at_end,
        payment_method=payment_method,
        visible_to_patient=visible_to_patient,
    )


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    payment_instr_form = PaymentInstructionCreateForm()
    if "save_created_payment_status" in request.form and payment_instr_form.validate_on_submit():
        PayTrack = PaymentTracker()
        payment_instr_form.populate_obj(PayTrack)
        PayTrack.author = current_user.id

        db.session.add(PayTrack)
        db.session.commit()

        flash(f"Payment Instruction #{PayTrack.id} created successfully.", "success")
        return redirect(url_for("payment_tracker_bp.instructions"))

    return render_template("payment_tracker/create.html", payment_instr_form=payment_instr_form)
