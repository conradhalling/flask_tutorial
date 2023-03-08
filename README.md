# flask_tutorial

## Introduction

This code implements the application created by the Flask 2.2.x tutorial at
https://flask.palletsprojects.com/en/2.2.x/tutorial/, with some improvements.

## Commands

### Initialize the Database

Change the working directory to the base directory (which contains the
`flaskr` subdirectory) and initialize or reinitialize the database with the
following command:

```shell
flask --app flaskr init-db
```

### Start the Application

Change the working directory to the base directory (which contains the
`flaskr` subdirectory) and run the application with the following command:

```shell
flask --app flaskr run --debug
```

## SQLite Database

Use the following commands to initialize the database to view the contents.

```
$ flask --app flaskr init-db
Initialized the database.
$ sqlite3 instance/flaskr.sqlite
SQLite version 3.39.5 2022-10-14 20:58:05
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE post (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
sqlite> .quit
```

## Versions

### Version 0.2.1

This version completes the _Define and Access the Database_ instructions at
https://flask.palletsprojects.com/en/2.2.x/tutorial/database/. I made
the following changes to the tutorial's code:

- Add additional code to enforce SQLite foreign key constraints for every
connection.

- Change column `post.author_id` to `post.user_id` for clarity.

- Revise file schema.sql to drop table `post` before dropping table `user`
since `post.user_id` references `user.id`.

### Version 0.1

This version completes the _Application Setup_ instructions at
https://flask.palletsprojects.com/en/2.2.x/tutorial/factory/.

The application displays "Hello, World!" at the URL
http://127.0.0.1:5000/hello.

## License

This repository uses the BSD 3-Clause License because that is the license used
by the Flask project.
