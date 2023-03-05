"""
Manage connections to the sqlite3 database.
"""

import sqlite3

import click
import flask


def get_db():
    """
    Return a connection to the database.

    Use the path defined in the configuration, and store the connection and
    its attributes in flask.g, a dictionary variable used by the request
    management code.
    """
    if "db" not in flask.g:
        # Get and store a connection to the database.
        flask.g.db = sqlite3.connect(
            flask.current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # Configure the connection to return data rows as dictionary-like
        # objects with indexed and case-insensitive named access to columns.
        flask.g.db.row_factory = sqlite3.Row
        # Enforce foreign key constraints.
        cursor = flask.g.db.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    return flask.g.db


def close_db(e=None):
    """
    Close the connection to the database.
    """
    # db is a sqlite3.Connection object.
    db = flask.g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """
    Modify the behavior of the app object.

    Tell Flask to call the close_db function when cleaning up after returning
    the response.

    Add the init_db_command function as a function that can be called with the
    "flask --app flaskr init-db" command.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def init_db():
    """
    Initialize the database by executing the commands in the schema.sql file.
    """
    # Get a connection to the database.
    db = get_db()
    # Open a resource, schema.sql, relative to the flaskr package.
    with flask.current_app.open_resource("schema.sql") as f:
        # Call the sqlite3.Connection.executescript method to execute the
        # commands in the schema.sql file.
        commands = f.read().decode("utf8")
        db.executescript(commands)


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
