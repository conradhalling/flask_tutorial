"""
There’s not much to test about the factory itself. Most of the code will be
executed for each test already, so if something fails the other tests will
notice.

"""

import flaskr

def test_config():
    """
    The only behavior that can change is passing test config. If config is not
    passed, there should be some default configuration, otherwise the
    configuration should be overridden.
    """
    assert not flaskr.create_app().testing
    assert flaskr.create_app({"TESTING": True}).testing

def test_hello(client):
    """
    You added the hello route as an example when writing the factory at the
    beginning of the tutorial. It returns “Hello, World!”, so the test checks
    that the response data matches.
    """
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
