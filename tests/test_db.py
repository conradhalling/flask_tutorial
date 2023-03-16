import sqlite3

import pytest

import flaskr.db


def test_get_close_db(app):
    """
    Within an application context, get_db should return the same connection
    each time it’s called. After the context, the connection should be closed.
    """
    with app.app_context():
        conn = flaskr.db.get_conn()
        assert conn is flaskr.db.get_conn()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        conn.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """
    The init-db command should call the init_db function and output a message.

    This test uses Pytest's monkeypatch fixture to replace the init_db
    function with one that records that it's been called. The runner fixture
    you wrote above is used to call the init-db command by name.
    """

    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("flaskr.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
