"""
Manage the "blog" blueprint.

The blog blueprint enables displaying blog posts by anyone (whether
logged in or not); and creating, editing and deleting blog posts by
a logged in user.
"""

import flask
import werkzeug

import flaskr.auth
import flaskr.db

# Create the blog blueprint without a url_prefix.
bp = flask.Blueprint("blog", __name__)


@bp.route("/")
def index():
    """
    Display the home page, which shows all blog posts and provides
    links for creating an account, logging in, logging out, and
    editing blog posts owned by the logged in user.
    """
    posts = flaskr.db.select_all_posts()
    return flask.render_template("blog/index.html.j2", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@flaskr.auth.login_required
def create():
    if flask.request.method == "POST":
        title = flask.request.form["title"]
        body = flask.request.form["body"]
        user_id = flask.g.user["id"]
        error = None
        if not title:
            error = "Title is required."
        # elif not body:
        #     error = "Content is required."
        if error is not None:
            flask.flash(error)
        else:
            flaskr.db.insert_post(title, body, user_id)
            return flask.redirect(flask.url_for("blog.index"))
    return flask.render_template("blog/create.html.j2")


def get_post(id, check_author=True):
    post = flaskr.db.select_post(id)
    if post is None:
        # The post does not exist.
        # Return a 404 Page Note Found error.
        werkzeug.exceptions.abort(404, f"Post id {id} doesn't exist.")
    if check_author and post["user_id"] != flask.g.user["id"]:
        # The post does not belong to the current user.
        # Return a 403 Forbidden error.
        werkzeug.exceptions.abort(403)
    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@flaskr.auth.login_required
def update(id):
    post = get_post(id)
    if flask.request.method == "POST":
        title = flask.request.form["title"]
        body = flask.request.form["body"]
        error = None
        if not title:
            error = "Title is required."
        # elif not body:
        #     error = "Content is required."
        if error is not None:
            flask.flash(error)
        else:
            flaskr.db.update_post(id, title, body)
            return flask.redirect(flask.url_for("blog.index"))
    return flask.render_template("blog/update.html.j2", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@flaskr.auth.login_required
def delete(id):
    # Make sure the post exists.
    get_post(id)
    # Delete the post and redirect to the index page.
    flaskr.db.delete_post(id)
    return flask.redirect(flask.url_for("blog.index"))
