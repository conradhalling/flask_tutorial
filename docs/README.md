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

### Clone the Source Code

Clone the source code from https://github.com/conradhalling/flask_tutorial.

### Install the flaskr Package

From within the flaskr_tutorial folder, install using pip:

```
pip install -e .
```

### Initialize the Database

Initialize or reinitialize the database with the following command:

```shell
flask --app flaskr init-db
```

### Start the Application

Start the application with the following command, where `--debug` is
optional.

```shell
flask --app flaskr run [--debug]
```

## License

This repository uses the BSD 3-Clause License because that is the license used
by the [Flask project](https://github.com/pallets/flask/).

## Links

- [Source Code](https://github.com/conradhalling/flask_tutorial)
- [Versions](versions.md)
- [SQLite Database](sqlite.md)
