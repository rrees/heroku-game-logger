import os
import logging

import flask
import flask_sslify

from . import handlers
from . import redis_utils
from . import context_processors

from app import auth

ENV = os.environ.get("ENV", "PROD")

redis_url = os.environ["REDIS_URL"]

redis = redis_utils.setup_redis(redis_url) if redis_url else None

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

if not ENV == "DEV":
    sslify = flask_sslify.SSLify(app)


logger = app.logger

# Uncomment to enable auth debugging info
LOGGING_FLAG = os.environ.get("LOGGING_FLAG", "WARNING")
if LOGGING_FLAG == "INFO":
    app.logger.setLevel(logging.INFO)

# Add template context processors here
# app.context_processor(context_processors.years)

routes = [
    ("/", "index", handlers.pages.front_page, ["GET"]),
    ("/home", "home", handlers.pages.home_page, ["GET"]),
    ("/log", "log_form", handlers.logs.log_form, ["POST"]),
    ("/logs", "logs_listing", handlers.logs.list, ["GET"]),
    ("/logs/tag/<tag_name>", "logs_by_tag", handlers.logs.list_by_tag, ["GET"]),
    ("/logs/year/<year>", "logs_by_year", handlers.logs.list_by_year, ["GET"]),
    ("/logs/recent", "recent_logs", handlers.logs.recent_logs, ["GET"]),
    ("/log/<log_id>", "show_log", handlers.logs.show_log, ["GET"]),
    ("/log/<log_id>/edit", "edit_log", handlers.logs.edit_log, ["GET"]),
    (
        "/log/<log_id>/forms/delete",
        "delete_log_form",
        handlers.logs.delete_log_form,
        ["POST"],
    ),
    (
        "/log/<log_id>/forms/edit",
        "edit_log_form",
        handlers.logs.edit_log_form,
        ["POST"],
    ),
    ("/log/add", "logs_add", handlers.pages.add_log, ["GET"]),
    ("/import", "import", handlers.transfers.import_logs, ["GET"]),
    ("/import/form", "import_form", handlers.transfers.import_logs_form, ["POST"]),
    ("/export", "export", handlers.transfers.export_logs, ["GET"]),
    ("/years", "years", handlers.pages.years, ["GET"]),
    ("/navigation/logs", "navigation_logs", handlers.navigation.logs, ["GET"]),
]

for path, endpoint, handler, methods in routes + auth.routes.all:
    app.add_url_rule(path, endpoint, handler, methods=methods)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception("An error occurred during a request.")
    return "An internal error occurred.", 500
