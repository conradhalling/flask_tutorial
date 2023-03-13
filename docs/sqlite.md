# SQLite Database

## Initialize the Database

Change the working directory to the base directory (which contains the
`flaskr` subdirectory) and initialize or reinitialize the database with the
following command:

```shell
flask --app flaskr init-db
```

## Explore the Database

After initializing and using the SQLite database, use the following commands
to view its contents:

```shell
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

sqlite> select * from tbl_user;
[output omitted]

sqlite> select * from tbl_post;
[output omitted]

sqlite> .quit
```
