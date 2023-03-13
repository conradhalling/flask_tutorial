import flask
import werkzeug

import flaskr.auth
import flaskr.db

# Create the blog blueprint without a url_prefix.
bp = flask.Blueprint("blog", __name__)


@bp.route("/")
def index():
    posts = select_all_posts()
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
        if not body:
            error = "Content is required."
        if error is not None:
            flask.flash(error)
        else:
            insert_post(title, body, user_id)
            return flask.redirect(flask.url_for("blog.index"))
    return flask.render_template("blog/create.html.j2")


def get_post(id, check_author=True):
    post = select_post(id)
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
        if not body:
            error = "Content is required."
        if error is not None:
            flask.flash(error)
        else:
            update_post(id, title, body)
            return flask.redirect(flask.url_for("blog.index"))
    return flask.render_template("blog/update.html.j2", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@flaskr.auth.login_required
def delete(id):
    # Make sure the post exists.
    get_post(id)
    # Delete the post and redirect to the index page.
    delete_post(id)
    return flask.redirect(flask.url_for("blog.index"))


# Database interaction code.
# Should these functions be moved into a different file?


def delete_post(post_id):
    sql1 = """
        DELETE FROM
            tbl_post
        WHERE
            id = ?
    """
    conn = flaskr.db.get_conn()
    conn.execute(sql1, (post_id,))
    conn.commit()


def insert_post(title, body, user_id):
    sql2 = """
        INSERT INTO tbl_post
        (title, body, user_id)
        VALUES (?, ?, ?)
    """
    conn = flaskr.db.get_conn()
    conn.execute(sql2, (title, body, user_id))
    conn.commit()


def select_all_posts():
    sql3 = """
        SELECT
            p.id,
            p.title,
            p.body,
            p.created,
            p.user_id,
            u.name
        FROM
            tbl_post p
            INNER JOIN tbl_user u
                ON p.user_id = u.id
        ORDER BY
            p.created DESC
    """
    conn = flaskr.db.get_conn()
    result_set = conn.execute(sql3)
    posts = result_set.fetchall()
    return posts


def select_post(post_id):
    sql4 = """
        SELECT
            p.id,
            p.title,
            p.body,
            p.created,
            p.user_id,
            u.name
        FROM
            tbl_post p
            INNER JOIN tbl_user u
                ON p.user_id = u.id
        WHERE
            p.id = ?
    """
    conn = flaskr.db.get_conn()
    result_set = conn.execute(sql4, (post_id,))
    post = result_set.fetchone()
    return post


def update_post(post_id, title, body):
    sql5 = """
        UPDATE
            tbl_post
        SET
            title = ?,
            body = ?
        WHERE
            id = ?
    """
    conn = flaskr.db.get_conn()
    conn.execute(sql5, (title, body, post_id))
    conn.commit()
