import functools
import datetime
from flask import redirect, url_for, flash, abort, current_app
from flask_login import LoginManager, current_user
from application.model import User
from application.logging import logger
from application.database import db

login_manager = LoginManager()

# login_manager.login_view = 'auth_bp.login'
# login_manager.login_message = 'Please Login to view this page.'
# login_manager.login_message_category = 'warning'
login_success_view_admin = "user_bp.index"
login_success_view_non_admin = "user_home_bp.index"
logout_success_view_admin = "auth_bp.login"
logout_success_view_non_admin = "store_front_bp.index"
# register_success_view = 'home_bp.index'


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.filter(User.username == user_id).first()
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth_bp.login"))


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not current_user.is_admin():
            abort(403)
        return view(**kwargs)

    return wrapped_view


def non_admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if current_user.is_admin():
            abort(403)
        return view(**kwargs)

    return wrapped_view


def create_first_admin_user_if_not_exist(app):
    with app.app_context():
        user = User.query.filter(User.admin == 1).first()
        if not user:
            logger.warn("No admin user found. Attempting to create one.")
            try:
                username = "root"
                password = "root"
                fullname = 'System Admin'
                new_user = User(
                    fullname=fullname,
                    username=username,
                    password=password,
                    admin=1,
                    active=1,
                    created_at=datetime.datetime.now(),
                    sex="O",
                    age="0y",
                )
                db.session.add(new_user)
                db.session.commit()
                logger.warn(f"Admin user > Fullname: {fullname} | Username: {username} | Password: {password}")
                logger.warn("First admin user created. Please change these credential on first login ASAP.")
            except Exception as e:
                logger.error(e)
                logger.error("Attempt to create first admin user failed.")
