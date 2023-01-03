from importlib import import_module
from flask import Flask, current_app, render_template
from flask_migrate import Migrate
from flask_minify import Minify
from flask_compress import Compress
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from application.database import db
from application.authentication import login_manager, create_first_admin_user_if_not_exist
from application.logging import logger


def action_on_teardown(exception=None):
    db.session.remove()


def http_error_handler(e):
    return render_template("layout/error.html", error=e)


def action_before_first_request():
    create_first_admin_user_if_not_exist(current_app)


def local_datetime(dttm, format="s"):
    if not dttm:
        return
    if not isinstance(dttm, datetime.datetime):
        dttm = datetime.datetime(dttm.year, dttm.month, dttm.day, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
    local_tzone = current_app.config["LOCAL_TIMEZONE"]
    local_timezone = pytz.timezone(local_tzone)
    if format == "s":  # short ISO like date time
        return dttm.replace(tzinfo=pytz.utc).astimezone(local_timezone).strftime("%Y-%m-%d %H:%M:%S")
    elif format == "l":  # long local format date time
        return dttm.replace(tzinfo=pytz.utc).astimezone(local_timezone).strftime("%c")
    elif format == "d":  # ISO date only
        return dttm.replace(tzinfo=pytz.utc).astimezone(local_timezone).strftime("%Y-%m-%d")
    elif format == "t":  # 24h time
        return dttm.replace(tzinfo=pytz.utc).astimezone(local_timezone).strftime("%H:%M:%S")
    elif format == "dd":  # long custom format datetime
        return dttm.replace(tzinfo=pytz.utc).astimezone(local_timezone).strftime("%A, %B %d, %Y")
    elif format == "a":  # time ago
        dif = relativedelta(
            datetime.datetime.now(datetime.timezone.utc), dttm.replace(tzinfo=pytz.utc).astimezone(pytz.utc)
        )
        ago = (
            " ".join(
                [
                    f"{dif.years} year" if dif.years else "",
                    f"{dif.months} month" if dif.months else "",
                    f"{dif.days} day" if dif.days else "",
                    f"{dif.hours} hour" if dif.hours else "",
                    f"{dif.minutes} min" if dif.minutes else "",
                    f"{dif.seconds} sec" if dif.seconds else "",
                ]
            )
            + " ago"
        )
        return ago
    elif format == "age":  # time ago
        dif = relativedelta(
            datetime.datetime.now(datetime.timezone.utc), dttm.replace(tzinfo=pytz.utc).astimezone(pytz.utc)
        )
        age = " ".join(
            [
                f"{dif.years} year" if dif.years else "",
                f"{dif.months} month" if dif.months else "",
                f"{dif.days} day" if dif.days else "",
            ]
        )
        return age


def context_processors():
    return {
        "utcnow": datetime.datetime.utcnow(),
        "copyright_year": int(datetime.datetime.utcnow().strftime("%Y")) + 10,
    }


def create_app(configuration):
    # Application setup
    app = Flask(__name__.split(".")[0], static_url_path=configuration.STATIC_DIR_PATH)
    app.config.from_object(configuration)

    # Extensions
    db.init_app(app)
    app.teardown_request(action_on_teardown)
    app.before_first_request(action_before_first_request)
    app.add_template_filter(local_datetime)
    app.context_processor(context_processors)
    login_manager.init_app(app)
    CSRFProtect(app)
    Migrate(app, db)
    Bootstrap5(app)
    # Register routes/apps
    for route in [
        "index",
        "admin",
        "medicine",
        "auth",
        "user_home",
        "dashboard",
        "user",
        "prescription",
        "conversation",
    ]:
        bp = import_module(f"application.routes.{route}").blueprint
        app.register_blueprint(bp)

    # Handle Error pages
    # 400 Bad Request
    # 401 Unauthorized
    # 403 Forbidden
    # 404 Not Found
    # 405 Method Not Allowed
    # 500 Internal Server Error
    for error_code in [400, 401, 403, 404, 405, 500]:
        app.register_error_handler(error_code, http_error_handler)

    # Content-Encoding: gz (compress) and minify
    if not app.debug:
        Compress(app)
        Minify(app=app, html=True, js=True, cssless=True)

    return app
