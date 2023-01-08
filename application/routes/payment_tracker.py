from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from application.authentication import admin_required
from application.database import db
from application.model import PaymentTracker, User
from application.form import PaymentInstructionForm, PaymentInstructionSearchForm
from sqlalchemy import exc
from application.helper import string_date_as_timezone




blueprint = Blueprint("payment_tracker_bp", __name__, url_prefix="/payment-tracker")


def list_payment_instruction(username, start_date, end_date, payment_status, payment_id):
    pass


def create_payment_instruction(username):
    pass


def delete_payment_instruction(payment_id):
    pass


def edit_payment_instruction(payment_id):
    pass


@blueprint.route("/instructions", methods=["GET", "POST"])
@login_required
@admin_required
def instructions():

    user_id = current_user.id
    page = request.args.get("page", 1, type=int)

    id = request.args.get("id", "", type=str).strip()
    patient_id = request.args.get("patient_id", "", type=str).strip()
    description = request.args.get("description", "", type=str).strip()
    payment_status = request.args.get("payment_status", "", type=str).strip()
    created_at_start = request.args.get("created_at_start", "", type=str).strip()
    created_at_end = request.args.get("created_at_end", "", type=str).strip()
    paid_at_start = request.args.get("paid_at_start", "", type=str).strip()
    paid_at_end = request.args.get("paid_at_end", "", type=str).strip()

    if "submit_filter" in request.form:
        
        id = request.form["id"] if request.form["id"] else id
        patient_id = request.form["patient_id"] if request.form["patient_id"] else patient_id
        description = request.form["description"] if request.form["description"] else description
        payment_status = request.form["payment_status"] if request.form["payment_status"] else payment_status
        created_at_start = request.form["created_at_start"] if request.form["created_at_start"] else created_at_start
        created_at_end = request.form["created_at_end"] if request.form["created_at_end"] else created_at_end
        paid_at_start = request.form["paid_at_start"] if request.form["paid_at_start"] else paid_at_start
        paid_at_end = request.form["paid_at_end"] if request.form["paid_at_end"] else paid_at_end
        
        url_query = f"?id={id}&patient_id={patient_id}&description={description}&payment_status={payment_status}&created_at_start={created_at_start}&created_at_end={created_at_end}&paid_at_start={paid_at_start}&paid_at_end={paid_at_end}"
        
        return redirect(url_for("payment_tracker_bp.instructions") + url_query)

    search_queries = []
    if id:
        search_queries.append((PaymentTracker.id == id))
    if patient_id:
        search_queries.append((PaymentTracker.patient_id == patient_id))
    if payment_status:
        search_queries.append((PaymentTracker.payment_status == payment_status))
    if description:
        search_queries.append((PaymentTracker.description == description))

    if created_at_start: created_at_start_tz = string_date_as_timezone(created_at_start, "%Y-%m-%d", "UTC")
    if created_at_end: created_at_end_tz = string_date_as_timezone(created_at_end, "%Y-%m-%d", "UTC")
    if paid_at_start: paid_at_start_tz = string_date_as_timezone(paid_at_start, "%Y-%m-%d", "UTC")
    if paid_at_end: paid_at_end_tz = string_date_as_timezone(paid_at_end, "%Y-%m-%d", "UTC")

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


    patients = User.query.filter(User.author == user_id).order_by(User.fullname).all()
    payment_instr = db.paginate(
        db.select(PaymentTracker).where(search_query).order_by(PaymentTracker.created_at), page=page, per_page=50
    )
    return render_template(
        "payment_tracker/index.html",
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
    payment_instr_form = PaymentInstructionForm()
    payment_instr_form.on_success_return_to_url.data = url_for("payment_tracker_bp.create")

    if "save_payment_status" in request.form and payment_instr_form.validate_on_submit():
        PayTrack = PaymentTracker()
        payment_instr_form.populate_obj(PayTrack)
        PayTrack.author = current_user.id
        db.session.add(PayTrack)
        db.session.commit()
        flash("Payment Instruction created.", "success")
        return redirect(payment_instr_form.on_success_return_to_url.data)

    return render_template("payment_tracker/create.html", payment_instr_form=payment_instr_form)


@blueprint.route("/delete/<id>", methods=["POST"])
@login_required
@admin_required
def delete(id):
    # obj = Medicine.query.filter(Medicine.id == id).one()
    # db.session.delete(obj)
    # db.session.commit()
    flash("Deleted successfully.", "success")
    return redirect(url_for("payment_tracker_bp.instructions"))


# @blueprint.route("/search", methods=["GET"])
# @login_required
# @admin_required
# def search():
#     user_id = current_user.id
#     search_arg = request.args.get("q", "", type=str)
#     search_query = (
#         (Medicine.author == user_id) & (Medicine.medicine.like(f"{search_arg}%"))
#         if search_arg != ""
#         else (Medicine.author == user_id)
#     )
#     query = db.select(Medicine).where(search_query)
#     result = db.session.execute(query)
#     names = [
#         {"key": row[0].short_name, "value": f"{row[0].medicine} {row[0].potency or '' }".strip()} for row in result
#     ]
#     return jsonify(names)


# @blueprint.route("/", methods=["GET"])
# @login_required
# @admin_required
# def index():
#     user_id = current_user.id
#     page = request.args.get("page", 1, type=int)
#     search_arg = request.args.get("search", "", type=str).strip()
#     search_query = (
#         (Medicine.author == user_id) & (Medicine.medicine.like(f"%{search_arg}%"))
#         if search_arg != ""
#         else (Medicine.author == user_id)
#     )
#     med = db.paginate(db.select(Medicine).where(search_query).order_by(Medicine.medicine), page=page, per_page=50)
#     return render_template("medicine/index.html", medicine=med, model=Medicine, search_arg=search_arg)


# @blueprint.route("/create", methods=["GET", "POST"])
# @login_required
# @admin_required
# def create():
#     med_form = MedicineForm()
#     if med_form.validate_on_submit():
#         new_med = Medicine()
#         new_med.medicine = med_form.medicine.data
#         new_med.short_name = med_form.short_name.data
#         new_med.potency = med_form.potency.data
#         new_med.author = current_user.id
#         try:
#             db.session.add(new_med)
#             db.session.commit()
#             flash("New medicine added.", "success")
#             return redirect(url_for("medicine_bp.index"))
#         except exc.IntegrityError:
#             db.session.rollback()
#             flash("Medicine/Short Name already exist.", "error")
#             return render_template("medicine/create.html", form=med_form)
#     return render_template("medicine/create.html", form=med_form)


# @blueprint.route("/delete/<id>", methods=["POST"])
# @login_required
# @admin_required
# def delete(id):
#     obj = Medicine.query.filter(Medicine.id == id).one()
#     db.session.delete(obj)
#     db.session.commit()
#     flash("Deleted successfully.", "success")
#     return redirect(url_for("medicine_bp.index"))
