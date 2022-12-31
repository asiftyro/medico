from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from application.authentication import admin_required
from application.database import db
from application.model import Medicine
from application.form import MedicineForm
from sqlalchemy import exc

blueprint = Blueprint("medicine_bp", __name__, url_prefix="/medicine")


@blueprint.route("/search", methods=["GET"])
@login_required
@admin_required
def search():
    user_id = current_user.id
    search_arg = request.args.get("q", "", type=str)
    search_query = (
        (Medicine.author == user_id) & (Medicine.medicine.like(f"{search_arg}%"))
        if search_arg != ""
        else (Medicine.author == user_id)
    )
    query = db.select(Medicine).where(search_query)
    result = db.session.execute(query)
    names = [{"key": row[0].short_name, "value": row[0].medicine} for row in result]
    return jsonify(names)


@blueprint.route("/", methods=["GET"])
@login_required
@admin_required
def index():
    user_id = current_user.id
    page = request.args.get("page", 1, type=int)
    search_arg = request.args.get("search", "", type=str).strip()
    search_query = (
        (Medicine.author == user_id) & (Medicine.medicine.like(f"%{search_arg}%"))
        if search_arg != ""
        else (Medicine.author == user_id)
    )
    med = db.paginate(db.select(Medicine).where(search_query).order_by(Medicine.medicine), page=page, per_page=50)
    return render_template("medicine/index.html", medicine=med, model=Medicine, search_arg=search_arg)


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    med_form = MedicineForm()
    if med_form.validate_on_submit():
        new_med = Medicine()
        new_med.medicine = med_form.medicine.data
        new_med.short_name = med_form.short_name.data
        new_med.author = current_user.id
        try:
            db.session.add(new_med)
            db.session.commit()
            flash("New medicine added.", "success")
            return redirect(url_for("medicine_bp.index"))
        except exc.IntegrityError:
            db.session.rollback()
            flash("Medicine/Short Name already exist.", "error")
            return render_template("medicine/create.html", form=med_form)
    return render_template("medicine/create.html", form=med_form)


@blueprint.route("/delete/<id>", methods=["POST"])
@login_required
@admin_required
def delete(id):
    obj = Medicine.query.filter(Medicine.id == id).one()
    db.session.delete(obj)
    db.session.commit()
    flash("Deleted successfully.", "success")
    return redirect(url_for("medicine_bp.index"))
