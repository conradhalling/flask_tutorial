# SQLite Database

## Initialize the Database

Change the working directory to the base directory (which contains the
`flaskr` subdirectory) and initialize or reinitialize the database with the
following command:

```shell
flask --app flaskr init-db
```

This creates or modifies the database file, which is located at
instance/flaskr.sqlite.

## Explore the Database

After initializing the SQLite database and using the flaskr application to
create a user and one or more blog posts, use the following commands to view
the contents of the database tables:

```
$ sqlite3 instance/flaskr.sqlite
SQLite version 3.39.5 2022-10-14 20:58:05
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE tbl_user (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE tbl_post (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES tbl_user (id)
);

sqlite> select * from tbl_user;
[output omitted]

sqlite> select * from tbl_post;
[output omitted]

sqlite> .quit
```
