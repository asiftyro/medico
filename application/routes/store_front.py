from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user


blueprint = Blueprint("store_front_bp", __name__, url_prefix="/store-front")


# Public route, open for all
@blueprint.route("/", methods=["GET"])
def index():
    return render_template("store_front/index.html")
