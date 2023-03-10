"""
Manage the auth blueprint.

The auth blueprint provides user interfaces for creating an account,
logging in, and logging out. It also updates flask.g.user before
a request, and it makes sure that the user is logged in.
"""

import functools
import sqlite3

import flask
import werkzeug

import flaskr.db

# Create the auth blueprint.
bp = flask.Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Register a new user in the database.

    When methood is not "POST", display the form for registering a new
    user. Otherwise, process the form request to register the user.

    If the user is registered successfully, redirect to the login
    page.

    If the user is not registered successfully, remain on the
    page and flash an error.
    """
    if flask.request.method == "POST":
        # Handle a POST request (the form was submitted).
        username = flask.request.form["username"]
        password = flask.request.form["password"]

        # Make sure that username and password are not empty.
        # The HTML code also enforces this.
        error = None
        if not username:
            error = "User name is required."
        elif not password:
            error = "Password is required."

        # Register the user in the database.
        if error is None:
            # Hash the password to increase security.
            hashed_password = werkzeug.security.generate_password_hash(password)
            try:
                flaskr.db.insert_user(username, hashed_password)
            except sqlite3.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # Redirect the user to the login page.
                return flask.redirect(flask.url_for("auth.login"))

        flask.flash(error)

    # Display the register page.
    return flask.render_template("auth/register.html.j2")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Attempt to log in the user.

    When methood is not "POST", display the form for registering a new
    user. Otherwise, process the form request to log in the user.

    If the user is unable to log in, display an error and remain on
    the page.

    If the user is able to log in, redirect to the index page.
    """
    # Get the user name and password and validate them against the values in
    # the database.
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        password = flask.request.form["password"]

        # Make sure that username and password are not empty.
        # The HTML also enforces this.
        error = None
        if not username:
            error = "User name is required."
        elif not password:
            error = "Password is required."

        # Select the user's credentials from the database using the name
        # value. The variable user contains a dict.
        user = flaskr.db.select_user_by_name(username)

        # Check that the user name and password are correct.
        error = None
        if user is None:
            # The user name was not found in the table.
            error = "Incorrect user name."
        elif not werkzeug.security.check_password_hash(user["password"], password):
            # The hashed password doesn't match what is stored in the
            # database.
            error = "Incorrect password."

        # If everything is okay, clear the old session, create a new session,
        # and redirect the user to the index page.
        if error is None:
            flask.session.clear()
            flask.session["user_id"] = user["id"]
            return flask.redirect(flask.url_for("index"))

        # An error occurred. Display it.
        flask.flash(error)

    # For a failed login request or when showing the page initially,
    # display the form for entering the user name and password.
    return flask.render_template("auth/login.html.j2")


@bp.route("/logout")
def logout():
    """
    Clear the session and redirect the user to the index page.
    """
    flask.session.clear()
    return flask.redirect(flask.url_for("index"))


@bp.before_app_request
def load_logged_in_user():
    """
    Register a function that runs before the view function, no matter what URL
    is requested.

    This updates flask.g.user to a dict containing the user's ID, name, and
    password, or to None if the user doesn't exist.
    """
    user_id = flask.session.get("user_id")
    if user_id is None:
        flask.g.user = None
    else:
        flask.g.user = flaskr.db.select_user_by_id(user_id)


def login_required(view_func):
    """
    Return a view function that checks if a user is loaded.

    This decorator returns a new view function that wraps the original view
    function that it's applied to. The new function checks if a user is loaded
    and redirects to the login page otherwise. If a user is loaded the
    original view function is called and continues normally.
    """

    @functools.wraps(view_func)
    def wrapped_view(**kwargs):
        if flask.g.user is None:
            # Redirect the user to the login page.
            return flask.redirect(flask.url_for("auth.login"))
        # Call the original view and continue normally.
        return view_func(**kwargs)

    return wrapped_view
