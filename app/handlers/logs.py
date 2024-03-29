import flask

from app import app
from app import users

from ..repositories import logs

def log_form():
    # app.logger.info(flask.request.form)
    logs.log(users.current_user_id(), flask.request.form)
    return flask.redirect(flask.url_for('home'))

def list():
    user_id = users.current_user_id()

    if not user_id:
        return flask.redirect(flask.url_for('index'))

    all_logs = logs.list(user_id)

    return flask.render_template('list.html', logs=all_logs)

def show_log(log_id):
    user_id = users.current_user_id()

    if not user_id:
        return flask.redirect(flask.url_for('index'))

    log = logs.read_log(user_id, log_id)

    return flask.render_template('log.html', log=log)

def edit_log(log_id):
    user_id = users.current_user_id()

    if not user_id:
        return flask.redirect(flask.url_for('index'))

    log = logs.read_log(user_id, log_id)

    return flask.render_template('log.html', log=log)

def delete_log_form(log_id):
    user_id = users.current_user_id()
    logs.delete_log(user_id, log_id, unconditional_delete=True)
    return flask.redirect(flask.url_for('logs_listing'))

def edit_log_form(log_id):
    user_id = users.current_user_id()
    logs.update_log(user_id, log_id, flask.request.form)
    return flask.redirect(flask.url_for('show_log', log_id=log_id))

def list_by_tag(tag_name):
    user_id = users.current_user_id()

    if not user_id:
        return flask.redirect(flask.url_for('index'))

    all_logs = logs.list_by_tag(user_id, tag_name)

    return flask.render_template('list.html', logs=all_logs)

def list_by_year(year):
    user_id = users.current_user_id()

    if not user_id:
        return flask.redirect(flask.url_for('index'))

    all_logs = logs.list_by_year(user_id, year)

    return flask.render_template('list.html', logs=all_logs)

def recent_logs():
    user_id = users.current_user_id()

    if not user_id:
        return flask.redirect(flask.url_for('index'))

    all_logs = logs.recent_logs()

    return flask.render_template('list.html', logs=all_logs)