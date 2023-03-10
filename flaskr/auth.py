"""
Manage the flask blueprint named "auth".
"""

import functools

import flask
import werkzeug

import flaskr.db

# Create the auth blueprint.
bp = flask.Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Register a new user in the database.
    """
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

        # Register the user in the database.
        if error is None:
            conn = flaskr.db.get_conn()
            try:
                sql1 = """
                    INSERT INTO tbl_user
                    (
                        name,
                        password
                    )
                    VALUES (?, ?)
                """
                conn.execute(
                    sql1,
                    (
                        username,
                        werkzeug.security.generate_password_hash(password),
                    ),
                )
                conn.commit()
            except conn.IntegrityError:
                error = f"User {username} is already registered."
                conn.rollback()
            else:
                # Redirect the user to the login page.
                return flask.redirect(flask.url_for("auth.login"))

        flask.flash(error)

    # Display the register page.
    return flask.render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Attempt to log the user in to the application.
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
        conn = flaskr.db.get_conn()
        sql2 = """
            SELECT
                id,
                name,
                password
            FROM
                tbl_user
            WHERE
                name = ?
        """
        result_set = conn.execute(sql2, (username,))
        user = result_set.fetchone()

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

        flask.flash(error)

    # For a failed login request or when showing the page initially,
    # display the form for entering the user name and password.
    return flask.render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """
    Clear the session and redirect the user to the index page, which will
    trigger a login request.
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
        conn = flaskr.db.get_conn()
        sql3 = """
            SELECT
                id,
                name,
                password
            FROM
                tbl_user
            WHERE
                id = ?
        """
        result_set = conn.execute(sql3, (user_id,))
        flask.g.user = result_set.fetchone()


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
