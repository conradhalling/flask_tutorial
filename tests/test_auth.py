"""
The register view should render successfully on GET. On POST with valid form
data, it should redirect to the login URL and the user's data should be in the
database. Invalid data should display error messages.

client.get() makes a GET request and returns the Response object returned by
Flask. Similarly, client.post() makes a POST request, converting the data dict
into form data.

To test that the page renders successfully, a simple request is made and
checked for a 200 OK status_code. If rendering failed, Flask would return a
500 Internal Server Error code.

headers will have a Location header with the login URL when the register view
redirects to the login view.

data contains the body of the response as bytes. If you expect a certain value
to render on the page, check that it's in data. Bytes must be compared to
bytes. If you want to compare text, use get_data(as_text=True) instead.

pytest.mark.parametrize tells Pytest to run the same test function with
different arguments. You use it here to test different invalid input and error
messages without writing the same code three times.
"""

import flask
import pytest

import flaskr.db


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register",
        data={
            "username": "a",
            "password": "a",
        },
    )
    assert response.headers["location"] == "/auth/login"

    with app.app_context():
        sql = "SELECT * FROM tbl_user WHERE name = 'a'"
        conn = flaskr.db.get_conn()
        rs = conn.execute(sql)
        assert rs.fetchone() is not None


@pytest.mark.parametrize(
    (
        "username",
        "password",
        "message",
    ),
    (
        (
            "",
            "",
            "User name is required.",
        ),
        (
            "a",
            "",
            "Password is required.",
        ),
        (
            "test",
            "test",
            "already registered",
        ),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register",
        data={
            "username": username,
            "password": password,
        },
    )
    # assert message in response.data
    assert message in response.get_data(as_text=True)


"""
The tests for the login view are very similar to those for register. Rather
than testing the data in the database, session should have user_id set after
logging in.
"""


def test_login(client, auth):
    """
    Using client in a with block allows accessing context variables such as
    session after the response is returned. Normally, accessing session
    outside of a request would raise an error.
    """
    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    assert response.headers["location"] == "/"

    with client:
        client.get("/")
        assert flask.session["user_id"] == 1
        assert flask.g.user["name"] == "test"


@pytest.mark.parametrize(
    (
        "username",
        "password",
        "message",
    ),
    (
        (
            "a",
            "test",
            "Incorrect user name",
        ),
        (
            "test",
            "a",
            "Incorrect password.",
        ),
    ),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.get_data(as_text=True)


"""
Testing logout is the opposite of login. session should not contain user_id
after logging out.
"""


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in flask.session
