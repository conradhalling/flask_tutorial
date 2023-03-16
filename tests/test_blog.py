"""
All the blog views use the auth fixture you wrote earlier. Call auth.login()
and subsequent requests from the client will be logged in as the test user.

The index view should display information about the post that was added with
the test data. When logged in as the author, there should be a link to edit
the post.

You can also test some more authentication behavior while testing the index
view. When not logged in, each page shows links to log in or register. When
logged in, there’s a link to log out.
"""

import pytest

import flaskr.db


def test_index(client, auth):
    # Not logged in.
    response = client.get("/")
    response_data = response.get_data(as_text=True)
    assert "Log In" in response_data
    assert "Register" in response_data

    # Logged in.
    auth.login()
    response = client.get("/")
    response_data = response.get_data(as_text=True)
    assert "Log Out" in response_data
    assert "test title" in response_data
    assert "by test on 2018-01-01" in response_data
    assert "test\nbody" in response_data
    assert 'href="/1/update"' in response_data


"""
A user must be logged in to access the create, update, and delete views. The
logged in user must be the author of the post to access update and delete,
otherwise a 403 Forbidden status is returned. If a post with the given id
doesn't exist, update and delete should return 404 Not Found.
"""


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        conn = flaskr.db.get_conn()
        conn.execute("UPDATE tbl_post SET user_id = 2 WHERE id = 1")
        conn.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403
    # current user doesn't see edit link
    assert 'href="/1/update"' not in client.get("/").get_data(as_text=True)


@pytest.mark.parametrize(
    "path",
    (
        "/2/update",
        "/2/delete",
    ),
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


"""
The create and update views should render and return a 200 OK status for a GET
request. When valid data is sent in a POST request, create should insert the
new post data into the database, and update should modify the existing data.
Both pages should show an error message on invalid data.
"""


def test_create(client, auth, app):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "body": ""})

    with app.app_context():
        conn = flaskr.db.get_conn()
        count = conn.execute("SELECT COUNT(id) FROM tbl_post").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", "body": ""})

    with app.app_context():
        conn = flaskr.db.get_conn()
        post = conn.execute("SELECT * FROM tbl_post WHERE id = 1").fetchone()
        assert post["title"] == "updated"


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    response_data = response.get_data(as_text=True)
    print(response_data)
    assert "Title is required." in response.get_data(as_text=True)


"""
The delete view should redirect to the index URL and the post should no longer
exist in the database.
"""


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        conn = flaskr.db.get_conn()
        post = conn.execute("SELECT * FROM tbl_post WHERE id = 1").fetchone()
        assert post is None
