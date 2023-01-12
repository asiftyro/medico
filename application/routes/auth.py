from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import logout_user, login_user, current_user, login_required
from application.authentication import (
    load_user,
    admin_required,
    login_success_view_admin,
    login_success_view_non_admin,
    logout_success_view_admin,
    logout_success_view_non_admin,
)
from application.form import LoginForm, ChangePasswordForm
from application.model import User
from application.database import db


blueprint = Blueprint("auth_bp", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for(login_success_view_admin))
        else:
            return redirect(url_for(login_success_view_non_admin))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = load_user(login_form.username.data)
        if user is None:
            flash("Please check your login details and try again (1).", "error")
        elif not user.check_password(login_form.password.data):
            flash("Please check your login details and try again (2).", "error")
        elif not user.is_active():
            flash("Your account is inactive. Please contact Administrator (3).", "error")
        else:
            login_user(user, remember=login_form.remember.data)
            flash("Logged In successfully.", "success")
            if user.is_admin():
                return redirect(url_for(login_success_view_admin))
            else:
                return redirect(url_for(login_success_view_non_admin))
    return render_template("auth/login.html", form=login_form)


@blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    was_admin = current_user.is_admin()
    logout_user()
    flash("Logged out. Please Login.", "info")
    if was_admin:
        return redirect(url_for(logout_success_view_admin))
    else:
        return redirect(url_for(logout_success_view_non_admin))


@blueprint.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Same routine used to change password for both logged in admin and non-admin user type.
    Password change form view differs based on user type.
    """
    user_id = current_user.id
    user = User.query.get(user_id)
    pwd_form = ChangePasswordForm()
    if pwd_form.validate_on_submit():
        user.password = pwd_form.password.data
        db.session.add(user)
        db.session.commit()
        flash("Password changed successfullly", "success")
        return redirect(url_for("auth_bp.change_password"))
    if current_user.is_admin():
        return render_template("auth/change_password.html", form=pwd_form)
    else:
        return render_template("user_home/change_password.html", form=pwd_form)


@blueprint.route("/change-password-on-behalf/<username>", methods=["GET", "POST"])
@login_required
@admin_required
def change_password_on_behalf(username):
    admin_id = current_user.id
    user = User.query.filter(User.username == username).first_or_404()
    pwd_form = ChangePasswordForm()
    if pwd_form.validate_on_submit():
        user.password = pwd_form.password.data
        user.author = admin_id
        db.session.add(user)
        db.session.commit()
        flash("Password changed successfully", "success")
        return redirect(url_for("user_bp.edit", username=username))
    elif request.method == "POST":
        flash("Password could not be changed. Please check form fields.", "error")

    return render_template("auth/change_password_on_behalf.html", user=user.to_dict(), pwd_form=pwd_form)
