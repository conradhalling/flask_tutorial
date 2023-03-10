DROP TABLE IF EXISTS tbl_post;
DROP TABLE IF EXISTS tbl_user;

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
