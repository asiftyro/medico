from flask import Blueprint, render_template, jsonify, current_app
from application.database import db
from flask_login import login_required, current_user
from application.authentication import admin_required
from application.model import Prescription
import datetime
import pytz

blueprint = Blueprint("dashboard_bp", __name__, url_prefix="/dashboard")


def start_and_end_of_last_7_days_in_str():
    local_tzone = current_app.config["LOCAL_TIMEZONE"]
    local_timezone = pytz.timezone(local_tzone)
    dt_ed = datetime.datetime.now().astimezone(local_timezone)
    dt_st = dt_ed - datetime.timedelta(days=6)
    return dt_st.strftime("%Y-%m-%d"), dt_ed.strftime("%Y-%m-%d")


@blueprint.route("/", methods=["GET"])
@login_required
@admin_required
def index():
    st, ed = start_and_end_of_last_7_days_in_str()
    res = db.session.query(Prescription).filter((Prescription.author==current_user.id) & (Prescription.follow_up_date==ed)).all()
    data = []
    for r in res:
        data.append({"id": r.id, "fullname": r.patient_desc.fullname, "username": r.patient_desc.username })
    
    return render_template("dashboard/index.html", follow_up_today = data)


@blueprint.route("/total-prescription", methods=["GET"])
@login_required
@admin_required
def total_prescription():
    sql = "select count(*) from prescription where author=:user_id"
    result = db.session.execute(sql, {"user_id": current_user.id}).fetchall()
    return jsonify({"count": result[0][0]})


@blueprint.route("/new-prescription-last-7-days", methods=["GET"])
@login_required
@admin_required
def new_prescription_last_7_days():
    st, ed = start_and_end_of_last_7_days_in_str()
    sql = (
        "select"
        " substr(created_at, 1, 10) as item_created_at,"
        " count(id) as item_count"
        " from prescription"
        " where author=:user_id"
        f" and substr(created_at, 1, 10) >= '{st}'"
        f" and substr(created_at, 1, 10) <= '{ed}'"
        " group by substr(created_at, 1, 10)"
        " order by 1 desc"
    )
    result = db.session.execute(sql, {"user_id": current_user.id}).fetchall()
    data = {}
    for row in result:
        data[row[0]] = row[1]
    return jsonify(data)


@blueprint.route("/total-patient", methods=["GET"])
@login_required
@admin_required
def total_patient():
    sql = "select count(*) from user where admin=0 and author=:user_id"
    result = db.session.execute(sql, {"user_id": current_user.id}).fetchall()
    return jsonify({"count": result[0][0]})


@blueprint.route("/new-patient-last-7-days", methods=["GET"])
@login_required
@admin_required
def new_patient_last_7_days():
    st, ed = start_and_end_of_last_7_days_in_str()
    sql = (
        "select"
        " substr(created_at, 1, 10) as item_created_at,"
        " count(id) as item_count"
        " from user"
        " where author=:user_id"
        " and admin=0"
        f" and substr(created_at, 1, 10) >= '{st}'"
        f" and substr(created_at, 1, 10) <= '{ed}'"
        " group by substr(created_at, 1, 10)"
        " order by 1 desc"
    )
    result = db.session.execute(sql, {"user_id": current_user.id}).fetchall()
    data = {}
    for row in result:
        data[row[0]] = row[1]
    return jsonify(data)

@blueprint.route("/follow_up_today", methods=["GET"])
@login_required
@admin_required
def follow_up_today():
    st, ed = start_and_end_of_last_7_days_in_str()
    res = db.session.query(Prescription).filter((Prescription.author==current_user.id) & (Prescription.follow_up_date==ed)).all()
    data = []
    for r in res:
        data.append({"id": r.id, "fullname": r.patient_desc.fullname, "username": r.patient_desc.username })
    return jsonify(data)
