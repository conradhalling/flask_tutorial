"""
Manage interactions with the sqlite3 database.
"""

import sqlite3

import click
import flask


def close_conn(e=None):
    """
    Close the connection to the database.
    """
    # conn is a sqlite3.Connection object.
    conn = flask.g.pop("conn", None)
    if conn is not None:
        conn.close()


def get_conn():
    """
    Return a connection to the database.

    Use the path defined in the configuration, and store the connection and
    its attributes in flask.g, a dictionary variable used by the request
    management code.
    """
    if "conn" not in flask.g:
        # Get and store a connection to the database.
        flask.g.conn = sqlite3.connect(
            flask.current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # Configure the connection to return data rows as dictionary-like
        # objects with indexed and case-insensitive named access to columns.
        flask.g.conn.row_factory = sqlite3.Row
        # Enforce foreign key constraints.
        sql1 = "PRAGMA foreign_keys=ON"
        flask.g.conn.execute(sql1)
    return flask.g.conn


def init_app(app):
    """
    Modify the behavior of the app object.

    Tell Flask to call the close_db function when cleaning up after returning
    the response.

    Add the init_db_command function as a function that can be called with the
    "flask --app flaskr init-db" command.
    """
    app.teardown_appcontext(close_conn)
    app.cli.add_command(init_db_command)


def init_db():
    """
    Initialize the database by executing the commands in the schema.sql file.
    """
    # Get a connection to the database.
    conn = get_conn()
    # Open a resource, schema.sql, relative to the flaskr package.
    with flask.current_app.open_resource("schema.sql") as f:
        # Call the sqlite3.Connection.executescript method to execute the
        # commands in the schema.sql file.
        commands = f.read().decode("utf8")
        conn.executescript(commands)


@click.command("init-db")
def init_db_command():
    """
    Initialize or reinitialize the database by creating new tables.

    This creates the instance/flaskr.sqlite file.

    Execute the CLI command as:
        flask --app flaskr init-db
    """
    init_db()
    click.echo("Initialized the database.")


# Database interaction code.
# Blog posts.


def delete_post(post_id):
    """
    Delete a blog post given its ID.

    Parameter
    ---------
    post_id : int
        The database ID of the post to delete.
    """
    sql = """
        DELETE FROM
            tbl_post
        WHERE
            id = ?
    """
    conn = get_conn()
    conn.execute(sql, (post_id,))
    conn.commit()


def insert_post(title, body, user_id):
    """
    Insert a blog post into the database.

    Parameters
    ----------
    title : str
        The title of the post
    body : str
        The body or text content of the post
    user_id : int
        The database ID of the user creating the post
    """
    sql = """
        INSERT INTO tbl_post
        (title, body, user_id)
        VALUES (?, ?, ?)
    """
    conn = get_conn()
    conn.execute(sql, (title, body, user_id))
    conn.commit()


def select_all_posts():
    """
    Return an iterable of dicts containing post attributes for all posts
    in the database.
    """
    sql = """
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
    conn = get_conn()
    result_set = conn.execute(sql)
    posts = result_set.fetchall()
    return posts


def select_post(post_id):
    """
    Return a dict containing post attributes for a specified post.

    Parameter
    ---------
    post_id : int
        The database ID of the request post
    """
    sql = """
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
    conn = get_conn()
    result_set = conn.execute(sql, (post_id,))
    post = result_set.fetchone()
    return post


def update_post(post_id, title, body):
    """
    Update a blog post in the database.

    Parameters
    ----------
    post_id : int
        The database ID of the post to be updated
    title : str
        The title of the post
    body : str
        The body or text content of the post
    """
    sql = """
        UPDATE
            tbl_post
        SET
            title = ?,
            body = ?
        WHERE
            id = ?
    """
    conn = get_conn()
    conn.execute(sql, (title, body, post_id))
    conn.commit()


# Users.


def insert_user(username, hashed_password):
    """
    Insert a new user into the database.

    Parameters
    ----------
    username : str
        the name of the user
    hashed_password : str
        the hashed version of the password

    Raises
    ------
    sqlite.IntegrityError
        when the user is already registered in the database
    """
    sql = """
        INSERT INTO tbl_user
        (
            name,
            password
        )
        VALUES (?, ?)
    """
    conn = get_conn()
    try:
        conn.execute(sql, (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise


def select_user_by_id(user_id):
    """
    Return a dict containing user attributes for a specified user.

    Parameter
    ---------
    user_id : int
        The database ID of the requested user
    """
    sql = """
        SELECT
            id,
            name,
            password
        FROM
            tbl_user
        WHERE
            id = ?
    """
    conn = get_conn()
    result_set = conn.execute(sql, (user_id,))
    user = result_set.fetchone()
    return user


def select_user_by_name(username):
    """
    Return a dict containing user attributes for a specified user.

    Parameter
    ---------
    username : str
        The name of the requested user
    """
    sql = """
        SELECT
            id,
            name,
            password
        FROM
            tbl_user
        WHERE
            name = ?
    """
    conn = get_conn()
    result_set = conn.execute(sql, (username,))
    user = result_set.fetchone()
    return user
