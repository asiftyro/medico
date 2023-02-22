from flask import Blueprint, redirect, url_for, flash, current_app, jsonify
from flask_login import current_user, login_required
from application.authentication import admin_required, non_admin_required
from application.database import db
from application.model import User, Conversation
from application.form import ConversationForm
import pytz


blueprint = Blueprint("conversation_bp", __name__, url_prefix="/conversation")

# TODO:
def get_conversation_for_admin():
    pass


# TODO:
def get_conversation_for_patient():
    pass


# TODO:
@blueprint.route("/patient/<username>", methods=["GET", "POST"])
@login_required
@non_admin_required
def send_conversation_from_patient(username):
    pass


@blueprint.route("/<username>", methods=["GET", "POST"])
@login_required
@admin_required
def send_conversation_from_admin(username):
    """Post new Admin Coversation and redirect to reatment page"""
    conv_form = ConversationForm()
    user = User.query.filter(User.username == username).first_or_404()
    author_id = current_user.id
    admin_id = current_user.id
    patient_id = user.id

    if conv_form.validate_on_submit():
        conversation_item = Conversation(
            conversation=conv_form.conversation.data, read=0, patient_id=patient_id, admin_id=admin_id, author=author_id
        )
        db.session.add(conversation_item)
        db.session.commit()
        flash("Message sent.", "success")
        return redirect(url_for("user_bp.treatment", username=username))
    return redirect(url_for("user_bp.treatment", username=username))


@blueprint.route("/set-read-status/<id>/<read_status>", methods=["GET"])
@login_required
@admin_required
def set_read_status(id, read_status):
    conversation_item = Conversation.query.get(id)
    read_status = 0 if read_status == "1" else 1
    conversation_item.read = read_status
    db.session.add(conversation_item)
    db.session.commit()
    conversation_item = Conversation.query.get(id)
    return str(conversation_item.read)


@blueprint.route("/get-unread", methods=["GET"])
@login_required
@admin_required
def get_unread():
    admin_id = current_user.id
    local_tzone = current_app.config["LOCAL_TIMEZONE"]
    local_timezone = pytz.timezone(local_tzone)
    conversation = (
        Conversation.query.filter(
            (Conversation.admin_id == admin_id) & (Conversation.read == 0) & (Conversation.author != admin_id)
        )
        .order_by(Conversation.created_at.desc())
        .limit(15)
    )

    return_json = []
    for c in conversation:
        return_json.append(
            {
                "id": c.id,
                "patient_id": c.patient_id,
                "patient_username": c.patient_desc.username,
                "patient_fullname": c.patient_desc.fullname,
                "conversation": c.conversation,
                "created_at": c.created_at.replace(tzinfo=pytz.utc)
                .astimezone(local_timezone)
                .strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    return jsonify(return_json)
