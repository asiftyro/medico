import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from application.model import User, Organization
from application.form import AdminSettingsForm, OrganizationForm
from application.authentication import admin_required
from application.database import db
from application.helper import save_logo_thumbnail

blueprint = Blueprint("admin_bp", __name__, url_prefix="/admin")


# @blueprint.route("/", methods=["GET", "POST"])
# @login_required
# @admin_required
# def organization():


@blueprint.route("/", methods=["GET", "POST"])
@login_required
@admin_required
def index():
    user = User.query.get(current_user.id)
    admin_form = AdminSettingsForm(obj=user)

    org = Organization.query.filter(Organization.author == current_user.id).first()
    prev_logo = ''
    update_org = None
    if not org:
        update_org = Organization()
    else:
        update_org = org
        prev_logo = org.logo
        update_org.logo = ''

    org_form = OrganizationForm(obj=update_org)

    if "save_admin_settings_form" in request.form and admin_form.validate_on_submit():
        user.username = admin_form.username.data
        user.fullname = admin_form.fullname.data
        user.dob = admin_form.dob.data
        user.sex = admin_form.sex.data
        user.blood = admin_form.blood.data
        user.email = admin_form.email.data
        user.address = admin_form.address.data
        db.session.commit()
        flash("Admin information saved successfully.", "success")
        return redirect(url_for("admin_bp.index"))

    if "save_organization_form" in request.form and org_form.validate_on_submit():
        if org_form.logo.data:
            new_logo_name = "logo.png"
            update_org.logo = new_logo_name
            org_logo_path = os.path.join(current_app.config["LOGO_DIR"], new_logo_name)
            save_logo_thumbnail(org_form.logo.data, org_logo_path)
        else:
            update_org.logo = prev_logo

        update_org.name = org_form.name.data
        update_org.title = org_form.title.data
        update_org.description = org_form.description.data
        update_org.address = org_form.address.data
        update_org.author = current_user.id
        db.session.add(update_org)
        db.session.commit()
        flash("Organization information saved successfully.", "success")
        return redirect(url_for("admin_bp.index"))
    return render_template("admin/index.html", admin_form=admin_form, org_form=org_form)
