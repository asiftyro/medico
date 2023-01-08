import re
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from application.authentication import admin_required
from application.database import db
from application.model import PaymentTracker, User
from application.form import PaymentInstructionCreateForm, PaymentInstructionEditForm
from application.helper import string_date_as_timezone


blueprint = Blueprint("payment_tracker_bp", __name__, url_prefix="/payment-tracker")


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

        db.session.add(PayTrack)
        db.session.commit()

        flash("Edited successfully.", "success")
        return redirect(url_for("payment_tracker_bp.edit", id=id))
    return render_template("payment_tracker/edit.html", payment_instr_edit_form=edit_form, paym_instr=PayTrack)


@blueprint.route("/change-payment-status/<id>", methods=["GET", "POST"])
@login_required
@admin_required
def change_payment_status(id):
    obj = PaymentTracker.query.filter(PaymentTracker.id == id).one()
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
    description = request.args.get("description", "", type=str).strip()
    payment_status = request.args.get("payment_status", "", type=str).strip()
    created_at_start = request.args.get("created_at_start", "", type=str).strip()
    created_at_end = request.args.get("created_at_end", "", type=str).strip()
    paid_at_start = request.args.get("paid_at_start", "", type=str).strip()
    paid_at_end = request.args.get("paid_at_end", "", type=str).strip()
    # Filter/Search form is submitted
    if "submit_filter" in request.form and request.method == "POST":
        id = request.form["id"] if request.form["id"] else id
        patient_id = request.form["patient_id"] if request.form["patient_id"] else patient_id
        description = request.form["description"] if request.form["description"] else description
        payment_status = request.form["payment_status"] if request.form["payment_status"] else payment_status
        created_at_start = request.form["created_at_start"] if request.form["created_at_start"] else created_at_start
        created_at_end = request.form["created_at_end"] if request.form["created_at_end"] else created_at_end
        paid_at_start = request.form["paid_at_start"] if request.form["paid_at_start"] else paid_at_start
        paid_at_end = request.form["paid_at_end"] if request.form["paid_at_end"] else paid_at_end
        # Build filter query string of page url
        url_query = f"?id={id}&patient_id={patient_id}&description={description}&payment_status={payment_status}&created_at_start={created_at_start}&created_at_end={created_at_end}&paid_at_start={paid_at_start}&paid_at_end={paid_at_end}"
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
    if description:
        search_queries.append((PaymentTracker.description == description))

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

    # Get Payment Instructiion from db
    payment_instr = db.paginate(
        db.select(PaymentTracker).where(search_query).order_by(PaymentTracker.created_at), page=page, per_page=25
    )

    # Get patient database
    patients = User.query.filter(User.author == user_id).order_by(User.fullname).all()

    # Remove 'page' argument if exists
    query_string = request.query_string.decode("utf-8")
    query_string = re.sub("&?page=[0-9]*", "", query_string)
    return_url = url_for("payment_tracker_bp.instructions") + "?" + query_string

    return render_template(
        "payment_tracker/index.html",
        return_url=return_url,
        payment_instr=payment_instr,
        patients=patients,
        id=id,
        patient_id=patient_id,
        description=description,
        payment_status=payment_status,
        created_at_start=created_at_start,
        created_at_end=created_at_end,
        paid_at_start=paid_at_start,
        paid_at_end=paid_at_end,
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

        flash("Payment Instruction created.", "success")
        return redirect(url_for("payment_tracker_bp.instructions"))

    return render_template("payment_tracker/create.html", payment_instr_form=payment_instr_form)
