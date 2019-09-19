import json
import requests
import random
from flask import Flask, request, render_template, Response, url_for
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from io import StringIO
from database import db

# create flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object("config.DevelopmentConfig")
app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]
app.config.update()

# init database
db.init_app(app)

# set up mail
mail = Mail(app)

# logger
logger = app.logger

# flask app routes
@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET", "POST"])
def index():
    """ Index page """
    return render_template(
        "index.html",
        today=get_date()
    )


@app.route("/longtask", methods=["GET", "POST"])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {"Location": url_for("taskstatus",
                                                  task_id=task.id)}


@app.route("/status/<task_id>")
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending..."
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", "")
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    
    # return json
    return jsonify(response)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(err):
    return render_template('500.html'), 500


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


# flask utility functions
def get_date():
    """ return date as string """
    return datetime.now().strftime("%c")


# clear all db sessions at the end of each request
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# send email
def send_email(to, subject, msg_body, **kwargs):
    """
    Send Mail function
    :param to:
    :param subject:
    :param template:
    :param kwargs:
    :return: celery async task id
    """
    msg = Message(
        subject,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[to, ]
    )
    msg.body = "EARL Dealer Demo UI Test"
    msg.html = msg_body
    send_async_email.delay(msg)


# template filters
@app.template_filter('formatdate')
def format_date(value):
    dt = value
    return dt.strftime('%Y-%m-%d %H:%M')


if __name__ == "__main__":
    app.start()
