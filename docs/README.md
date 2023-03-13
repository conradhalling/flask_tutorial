# flask_tutorial

## Introduction

This code implements the flaskr application created by the
[Flask 2.2.x Tutorial](https://flask.palletsprojects.com/en/2.2.x/tutorial/),
with some modifications.

During development, the application is located at http://127.0.0.1:5000/. This
version, v0.4, allows the user to do the following:

- view existing blog posts
- create an account
- log in or out
- create, edit, or delete a blog post

## Installation

Clone the source code from https://github.com/conradhalling/flask_tutorial.
Follow the directions below to initialize the database and start the
application in development mode.

### Install Dependencies

These instructions assume you have used pyenv to install Python 3.11.1 and
you have cloned the code into ~/src/flask_tutorial.

Execute the following commands to set up a virtual environment and install
Flask.

	$ pyenv global 3.11.1
	$ cd ~/src/flask_tutorial
	$ python3 -m venv venv
	$ source venv/bin/activate
	$ pip3 install -U pip
	Successfully installed pip-23.0.1
	$ pip3 install -U setuptools
	Successfully installed setuptools-67.4.0
	$ pip3 install flask
	Successfully installed Jinja2-3.1.2 MarkupSafe-2.1.2 Werkzeug-2.2.3 click-8.1.3 flask-2.2.3 itsdangerous-2.1.2

### Initialize the Database

Change the working directory to the base directory (which contains the
`flaskr` subdirectory) and initialize or reinitialize the database with the
following command:

```shell
flask --app flaskr init-db
```

### Start the Application

Change the working directory to the base directory (which contains the
`flaskr` subdirectory) and start the application with the following command:

```shell
flask --app flaskr run --debug
```

## License

This repository uses the BSD 3-Clause License because that is the license used
by the [Flask project](https://github.com/pallets/flask/).

## Links

- [Source Code](https://github.com/conradhalling/flask_tutorial)
- [Versions](versions.md)
- [SQLite Database](sqlite.md)
