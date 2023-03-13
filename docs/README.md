# flask_tutorial

## Introduction

This code implements the flaskr application created by the
[Flask 2.2.x Tutorial](https://flask.palletsprojects.com/en/2.2.x/tutorial/),
with some improvements.

Get the source code at https://github.com/conradhalling/flask_tutorial.

## Web Interface

During development, the application is located at
http://127.0.0.1:5000/auth/login. This version (v0.3) allows you to
register a new user at http://127.0.0.1:5000/auth/register. Other
functionality (logging in, going to the home page, etc.) is broken in this
version but will be added in version 0.4.

## Command Line Interface

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

- [Versions](versions.md)
- [SQLite Database](sqlite.md)
