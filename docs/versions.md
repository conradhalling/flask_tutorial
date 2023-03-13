
# Versions

Versions are listed in reverse chronological order.

## Version 0.3

This version completes the following instructions:

- [_Blueprints and Views_](https://flask.palletsprojects.com/en/2.2.x/tutorial/views/)
- [_Templates_](https://flask.palletsprojects.com/en/2.2.x/tutorial/templates/)
- [_Static Files_](https://flask.palletsprojects.com/en/2.2.x/tutorial/static/)

This version adds the flask blueprint named `auth` for authenticating a user,
the Jinja2 HTML template files for the
[auth/login](http://127.0.0.1:5000/auth/login) and
[auth/register](http://127.0.0.1:5000/auth/register) pages, and the static CSS
file for styling the application.

I made the following changes to the tutorial's code:

- Rename the database tables from `user` to `tbl_user` and from `post` to
`tbl_post`.

- Use an absolute import for the `flaskr.db` module.

- Revise the code for database queries to separate the individual steps.

- For the `login` function, check that the username and password fields are not empty.

- Rename `flask.g.db` to `flask.g.conn`, for clarity.

## Version 0.2.1

This version completes the following instructions:

- [_Define and Access the Database_](https://flask.palletsprojects.com/en/2.2.x/tutorial/database/)

This version adds the code for initializing the database.
I made the following changes to the tutorial's code:

- Use minimal imports to make it clear what package or module is being
used for every call.

- Add additional code to enforce SQLite foreign key constraints for every
connection.

- Change column `post.author_id` to `post.user_id` for clarity.

- Revise the schema.sql file to drop table `post` before dropping table `user`
since `post.user_id` references `user.id`.

- Change column `user.username` to `user.name` to avoid redundancy.

## Version 0.1

This version completes the following instructions:

-  [_Application Setup_](https://flask.palletsprojects.com/en/2.2.x/tutorial/factory/)

This version contains the minimal code for starting and running the application.
The application displays "Hello, World!" at the URL
http://127.0.0.1:5000/hello.
