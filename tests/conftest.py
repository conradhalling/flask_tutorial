"""
This file contains setup functions called fixtures that each test will use.
Tests are in Python modules that start with test_, and each test function
in those modules also starts with test_.

Each test will create a new temporary database file and populate some data
that will be used in the tests. Write a SQL file to insert that data.

The app fixture will call the factory and pass test_config to configure
the application and database for testing instead of using your local
development configuration.

Pytest uses fixtures by matching their function names with the names of
arguments in the test functions. For example, the test_hello function you’ll
write next takes a client argument. Pytest matches that with the client
fixture function, calls it, and passes the returned value to the test
function.
"""

import os
import tempfile

import pytest

import flaskr
import flaskr.db

# Read the SQL commands from tests/data.sql.
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf-8")


@pytest.fixture
def app():
    """
    tempfile.mkstemp() creates and opens a temporary file, returning the file
    descriptor and the path to it. The DATABASE path is overridden so it
    points to this temporary path instead of the instance folder. After
    setting the path, the database tables are created and the test data is
    inserted. After the test is over, the temporary file is closed and
    removed.

    TESTING tells Flask that the app is in test mode. Flask changes some
    internal behavior so it’s easier to test, and other extensions can also
    use the flag to make testing them easier.
    """
    db_fd, db_path = tempfile.mkstemp()
    app = flaskr.create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )

    with app.app_context():
        # Initialize the database tables.
        flaskr.db.init_db()
        # Insert the test data into the database tables.
        # conn.executescript() commits the changes automatically.
        conn = flaskr.db.get_conn()
        conn.executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """
    The client fixture calls app.test_client() with the application object
    created by the app fixture. Tests will use the client to make requests
    to the application without running the server.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    The runner fixture is similar to client. app.test_cli_runner() creates
    a runner that can call the Click commands registered with the application.
    """
    return app.test_cli_runner()


"""
Authentication

For most of the views, a user needs to be logged in. The easiest way to do
this in tests is to make a POST request to the login view with the client.
Rather than writing that out every time, you can write a class with methods
to do that, and use a fixture to pass it the client for each test.
"""


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login",
            data={
                "username": username,
                "password": password,
            },
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """
    With the auth fixture, you can call auth.login() in a test to log in as
    the test user, which was inserted as part of the test data in the app
    fixture.
    """
    return AuthActions(client)
