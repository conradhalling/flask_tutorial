"""
Create and configure the Flask application.
"""

import os

import flask

import flaskr.auth
import flaskr.blog
import flaskr.db


def create_app(test_config=None):
    """
    Create and configure the application.
    """
    # Create a secret key value with this command:
    #   python -c 'import secrets; print(secrets.token_hex())'
    # The secret key is used for session cookies, so don't create a new
    # secret key every time you start the app.
    # See https://flask.palletsprojects.com/en/2.2.x/config/ for the
    # instance_relative_config parameter. When the argument is True,
    # configuration file paths are relative to the instance folder, which
    # can be obtained from app.instance_path.
    # Set the DATABASE configuration to the path to the flaskr.sqlite database
    # file, which becomes instance/flaskr.sqlite.
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="4b1e098f0392a9258ec753120bcb15b3c63cb960520a9458a601429dbe6fd7e0",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    # Override the default configuration using the test_config argument,
    # which is a dictionary of keys and values.
    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        # Here, the configuration is obtained from instance/config.py.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists outside of the flaskr directory.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # # Add a simple page that says "hello".
    # @app.route("/hello")
    # def hello():
    #     return "Hello, World!"

    # Modify the app object so it can close the database connection and
    # execute the "flask --app flaskr init-db" command from the CLI.
    flaskr.db.init_app(app)

    # Add the blueprints.
    app.register_blueprint(flaskr.auth.bp)
    app.register_blueprint(flaskr.blog.bp)

    # Any reference to endpoint "index" is routed to "/", which is mapped to
    # flaskr.blog.index in flaskr/blog.py.
    app.add_url_rule("/", endpoint="index")

    return app
