"""
Manage connections to the sqlite3 database.
"""

import sqlite3

import click
import flask


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


def close_conn(e=None):
    """
    Close the connection to the database.
    """
    # conn is a sqlite3.Connection object.
    conn = flask.g.pop("conn", None)
    if conn is not None:
        conn.close()


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
