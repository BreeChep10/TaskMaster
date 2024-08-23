#!/usr/bin/python3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import EmailNotValidError, validate_email
from flask import Flask, flash, redirect, render_template, request, sessions, url_for
from flask import make_response, jsonify
from flask_cors import CORS
from flask_login import login_manager, current_user
from itsdangerous import URLSafeTimedSerializer
import flask_login
import models
import os
import uuid
from os import getenv
from models.subtask import Subtask
from models.comment import TaskComment, ProjectComment
from models.task import Task
from models.project import Project
from models.timer import Timer
from models.user import User
# from quickstart import create_message, get_credentials, main, send_message
from werkzeug.utils import secure_filename


app = Flask(__name__)
SECRET_KEY = "eadff6d69ff0eb846bb982cb936f1bb20f48c091f04664378fd1c2de1769aa4c"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = "dp_uploads"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = models.storage.all("User").values()
login_tokens = []
serializer = URLSafeTimedSerializer(SECRET_KEY)
cache_id = str(uuid.uuid4())
CORS(app, resources={r"/*": {"origins": "*"}})



@login_manager.user_loader
def user_loader(id):
    """
    load a user from the database
    """
    for i in models.storage.all("User").values():
        if i.id == id:
            return i
    return None

@app.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Returns the status of the user
    """
    if current_user.is_authenticated:
        data = {
            "status": "logged",
            "id": current_user.id
        }

        return make_response(jsonify(data), 200)
    else:
        return make_response(jsonify({"status": "anonymous"}), 200)
    


@app.teardown_appcontext
def close_db(error):
    """
    Closes the current sqlalchemy session
    """
    models.storage.close()


@app.route("/", strict_slashes=False)
def taskmaster():
    """
    LANDING PAGE FOR TASKMASTER
    """
    return render_template("landing_page.html", cache_id=cache_id)



@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
@app.route("/login/<token>", strict_slashes=False)
def login(token=None):
    """
    Handles user login.

    Args:
        token (str, optional): A token for user authentication. Defaults to None.

    Returns:
        str: The rendered login template or a redirect to the cuisine route.

    Raises:
        Exception: If there is an error in unsealing the token.

    """
    if request.method == "GET":
        if request.referrer:
            if request.referrer.split("/")[-1] == "login":
                return render_template("login.html", invalid=True, cache_id=cache_id)

        if token:
            try:
                unsealed = serializer.loads(token, max_age=300)
                new = User(**unsealed)
                new.save()
                print(unsealed)
            except Exception as e:
                print("Error in unsealing", e)
        return render_template("login.html", invalid=False, cache_id=cache_id)

    elif request.method == "POST":
        submitted_email = request.form["email"]
        submitted_password = request.form["password"]
        remember_me = False

        user = None
        for i in models.storage.all("User").values():
            if i.email == submitted_email and i.password == submitted_password:
                user = i

        if user is None:
            return redirect(url_for("login"))

        try:
            if request.form["checkbox"] == "on":
                remember_me = True
        except Exception:
            pass
        flask_login.login_user(user, remember=remember_me)
        return redirect(url_for("cuisine"))






















if __name__ == "__main__":
    """
    Main Function
    """
    app.run(host="0.0.0.0", port=5001, debug=True)