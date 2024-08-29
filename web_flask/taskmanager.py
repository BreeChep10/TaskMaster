#!/usr/bin/python3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, flash, redirect, render_template, request, session, url_for, make_response, jsonify
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from itsdangerous import URLSafeTimedSerializer
import flask_login
import models
import os
import uuid
from os import getenv
from datetime import datetime
from models import task
from models.subtask import Subtask
from models.comment import TaskComment, ProjectComment
from models.task import Task
from models.project import Project
from models.timer import Timer
from models.user import User
from werkzeug.utils import secure_filename

# Initialize the Flask app
app = Flask(__name__)
SECRET_KEY = "eadff6d69ff0eb846bb982cb936f1bb20f48c091f04664378fd1c2de1769aa4c"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = "dp_uploads"

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Specifies the login view for unauthorized users

# Initialize CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Other configurations and initializations
users = models.storage.all("User").values()
login_tokens = []
serializer = URLSafeTimedSerializer(SECRET_KEY)
cache_id = str(uuid.uuid4())

# User loader callback for Flask-Login
@login_manager.user_loader
def user_loader(user_id):
    """
    Load a user from the database based on the given ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The user object if found, None otherwise.
    """
    return models.storage.get("User", user_id)  # Fetch user by ID

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
    Closes the current SQLAlchemy session
    """
    models.storage.close()

# ---------------WEB PAGES ----------------------
@app.route("/", strict_slashes=False)
def taskmaster():
    """
    LANDING PAGE FOR TASKMASTER
    """
    return render_template("landing_page.html", cache_id=cache_id, user=current_user)



@app.route("/logout", methods=["GET"], strict_slashes=False)
@login_required
def logout():
    """
    Logs out the current user.
    """
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("taskmaster"))


@app.route("/login", methods=["GET", "POST"])
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
        print("Get method")
        return render_template("login.html", invalid=False, cache_id=cache_id, user=current_user)


    elif request.method == "POST":
        # Handle POST request - process login
        submitted_email = request.form.get("email")
        submitted_password = request.form.get("password")
        remember_me = 'checkbox' in request.form
        print(submitted_email)
        print(submitted_password)

        # Query user by email
        user = next((u for u in models.storage.all("User").values() if u.email == submitted_email), None)
        if user:
            print(user)

        if user and user.password == submitted_password:
            login_user(user, remember=remember_me)
            flash("Logged in successfully.", "success")
            return redirect(url_for("taskmaster"))  # Redirect to a protected route
        else:
            flash("Invalid email or password.", "danger")
            return render_template("login.html", invalid=True, cache_id=cache_id)



@app.route("/signup", methods=["GET", "POST"], strict_slashes=False)
def signup():
    """
    Handles user signup.

    This function handles the user signup process. It receives a POST request with user information
    such as email, password, first name, and last name. It validates the input data,
    checks if the email is already registered, and creates a new user if the data is valid.

    Returns:
        If the request method is POST and the data is valid, it redirects to the login page.
        If the request method is GET or the data is invalid, it renders the "signup.html" template with appropriate
        error messages.
    """
    invalid_email = False
    existing_user = False
    user_created = False

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        
        # Check if the user already exists
        user = next((u for u in models.storage.all("User").values() if u.email == email), None)

        if user:
            existing_user = True
            return render_template("signup_page.html", existing=existing_user, cache_id=cache_id)
        else:
            # If the email is valid, create a new user object
            new_user = User(email=email, password=password, firstname=firstname, lastname=lastname)
                
            # Save the new user to the storage
            new_user.save()
            user_created = True

            return redirect(url_for("login"))

    # Render the signup page with the necessary flags
    return render_template("signup_page.html",
                           existing=existing_user,
                           invalid_email=invalid_email,
                           user_created=user_created,
                           cache_id=cache_id)



@login_required
@app.route("/projects", methods=["GET"], strict_slashes=False)
def projects_page():
    """
    PROJECTS PAGE
    """
    try:
        projects = [k for k in models.storage.all("Project").values() if k.user_id == current_user.id]
        projects = sorted(projects, key=lambda k: k.created_at)
        projects.reverse()
        return render_template("project_page.html", cache_id=cache_id, user=current_user, projects=projects)
    except Exception as e:
        print(e)
        return render_template("project_page.html", cache_id=cache_id, user=current_user, projects=[])

@app.route("/view_project", methods=["GET", "POST"], strict_slashes=False)
def view_project():
    """
    Project details and tasks
    """
    project_id = request.args.get("project_id", None)
    if not project_id:
        return redirect(url_for("projects_page"))
    else:
        project = models.storage.get("Project", project_id)
        tasks = project.tasks
        if not project:
            return redirect(url_for('projects_page'))
        return render_template("task_page.html",
                               user=current_user, cache_id=cache_id,
                               project=project,
                               tasks=tasks)


@app.route("/create_project", methods=["POST"], strict_slashes=False)
def create_project():
    if request.method == "POST" and current_user.is_authenticated:
        name = request.form.get("name")
        user_id = current_user.id
        description = request.form.get("description")
        new_project = Project(name=name,
                              user_id=user_id,
                              description=description)
        new_project.save()
        return redirect(url_for("projects_page"))


@app.route("/get_tasks", methods=["GET"], strict_slashes=False)
def get_tasks():
    project_id = request.args.get("project_id", None)
    project = models.storage.get("Project", project_id)
    tasks = project.tasks
    return jsonify([task.to_dict() for task in tasks])


@app.route("/save_task", methods=["POST"], strict_slashes=False)
def save_task():
    """
    Save a task
    """
    data = request.get_json()
    task_id = data.get("task_id")
    task = models.storage.get("Task", task_id)
    task.name = data.get("name")
    task.description = data.get("description")
    task.taskpriority = data.get("taskpriority")
    task.save()
    return jsonify({"save": "success"})

@app.route("/delete_task", methods=["POST"], strict_slashes=False)
def delete_task():
    """
    Deletes a task
    """
    data = request.get_json()
    task_id = data.get("task_id")
    task = models.storage.get("Task", task_id)
    task.delete()
    return jsonify({"delete": "success"})


@app.route("/create_task", methods=["POST", "GET"])
def create_task():
    project_id = request.args.get("project_id", None)
    project = None
    if project_id:
        project = models.storage.get("Project", project_id)
        if project:
            name = request.form.get("task-name")
            description = request.form.get("task-description")
            priority = request.form.get("task-priority")
            due_date = request.form.get("task-due-date")
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
            user_id = project.user_id

            task = Task(name=name,
                        description=description,
                        taskpriority=priority,
                        due_date=due_date,
                        user_id=user_id,
                        project_id=project_id)
            task.save()

            timer = Timer(task_id=task.id, end_time=due_date)
            timer.save()

            print(due_date)
            return redirect(request.referrer)


if __name__ == "__main__":
    """
    Main Function
    """
    app.run(host="127.0.0.1", port=5001, debug=True)
