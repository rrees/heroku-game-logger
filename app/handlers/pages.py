import datetime

import flask

from app import app


def front_page():
    app.logger.info(flask.session.keys())
    if "session_id" in flask.session:
        return flask.redirect(flask.url_for("home"))

    return flask.render_template("index.html")


def home_page():
    if not "session_id" in flask.session:
        return flask.redirect(flask.url_for("index"))

    return flask.render_template("home.html", today=datetime.date.today().isoformat())


def add_log():
    if not "session_id" in flask.session:
        return flask.redirect(flask.url_for("index"))

    return flask.render_template(
        "add-log.html", today=datetime.date.today().isoformat()
    )


def years():
    if not "session_id" in flask.session:
        return flask.redirect(flask.url_for("index"))

    first_year = 2016
    current_year = datetime.date.today().year

    years = [str(y) for y in range(current_year, first_year - 1, -1)]

    return flask.render_template("years.html", years=years)
