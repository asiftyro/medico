import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import current_user, login_required
from application.authentication import non_admin_required
from application.model import User, Conversation, Prescription, PaymentTracker
from application.form import ConversationForm, ChangePasswordForm
from application.database import db
from application.logging import logger
from application.helper import get_unique_id, save_conversation_photo_thumbnail
import pathlib

blueprint = Blueprint("user_home_bp", __name__, url_prefix="/user-home")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
@non_admin_required
def index():
    """Patient user view: User(Patient), Prescription, Conversation, Unpaid Bill from PaymentTracker."""
    """Conversation post by user(patient)."""
    user_id = current_user.id
    user = User.query.get(user_id)
    admin_id = user.author

    prescription = (
        Prescription.query.filter(Prescription.patient_id == user_id)
        .order_by(Prescription.id.desc())
        .all()
    )

    conversation = (
        Conversation.query.filter(Conversation.patient_id == user_id)
        .order_by(Conversation.id.desc())
        .all()
    )

    unread_conversation_count = 0
    for c in conversation:
        if c.read == 0 and (c.author == c.admin_id):
            unread_conversation_count += 1

    payment = (
        PaymentTracker.query.filter((PaymentTracker.patient_id == user_id) & (PaymentTracker.visible_to_patient==1))
        .order_by(PaymentTracker.id.desc())
        .all()
    )

    unpaid_bill_count = 0
    unpaid_bill_amount = 0
    for p in payment:
        if not p.payment_status:
            unpaid_bill_count += 1
            unpaid_bill_amount += p.amount
    

    conv_form = ConversationForm()
    if conv_form.validate_on_submit():
        conv_attach = conv_form.conversation_attachment.data
        uniq_attach_name = ""
        attach_type = ""
        if conv_attach:
            ext = pathlib.Path(conv_attach.filename).suffix
            if ext in [".jpg", ".png", ".jpeg"]:
                uniq_attach_name = get_unique_id() + ".png"
                attach_path = os.path.join(current_app.config["CONVERSATION_PHOTO_DIR"], uniq_attach_name)
                save_conversation_photo_thumbnail(conv_attach, attach_path)
                attach_type = "image"
            else:
                uniq_attach_name = get_unique_id() + ext
                attach_path = os.path.join(current_app.config["CONVERSATION_PHOTO_DIR"], uniq_attach_name)
                conv_attach.save(attach_path)
                attach_type = "video"

        conversation_item = Conversation(
            conversation=conv_form.conversation.data,
            conversation_attachment=uniq_attach_name,
            conversation_attachment_type=attach_type,
            read=0,
            patient_id=user_id,
            admin_id=admin_id,
            author=user_id,
        )

        db.session.add(conversation_item)
        db.session.commit()
        flash("Message sent.", "success")
        return redirect(url_for("user_home_bp.index"))

    return render_template(
        "user_home/index.html",
        user=user.to_dict(),
        payment=payment,
        conversation=conversation,
        prescription=prescription,
        unread_conversation_count=unread_conversation_count,
        unpaid_bill_count=unpaid_bill_count,
        unpaid_bill_amount=unpaid_bill_amount,
        form=conv_form,
    )


@blueprint.route("/set-conversation-as-read/<convId>", methods=["GET"])
@login_required
@non_admin_required
def set_conversation_as_read(convId):
    conv = Conversation.query.get(convId)
    conv.read = 1
    db.session.add(conv)
    db.session.commit()
    return "OK"


@blueprint.route("/delete-conversation", methods=["POST"])
@login_required
@non_admin_required
def delete_conversation():
    id = request.form['id']
    conv = Conversation.query.get(id)
    if not conv:
        abort(401)
    if current_user.id != conv.author:
        abort(401)

    db.session.delete(conv)
    db.session.commit()
    flash("Message deleted.", "success")
    return redirect(url_for('user_home_bp.index'));

@blueprint.route("/change-password", methods=["GET", "POST"])
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
        flash("Password changed successfully", "success")
        return redirect(url_for("user_home_bp.index"))
    elif request.method == "POST":
        flash("Password could not be changed. Please check form fields.", "error")
    return render_template("user_home/user_change_password.html", user=user.to_dict(), form=pwd_form)
