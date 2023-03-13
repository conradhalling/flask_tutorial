
# Versions

Versions are listed in reverse chronological order.

## Version 0.4

This version completes the following steps of the tutorial:

- [Blog Blueprint](https://flask.palletsprojects.com/en/2.2.x/tutorial/blog/)

During development, the application is available at http://127.0.0.1:5000/.

This version provides the complete user interface, which includes:

- viewing existing blog posts
- creating an account
- logging in or out
- creating, editing, or deleting a blog post

Code changes include:

- Add a flask blueprint named `blog` for displaying, creating, editing,
  and deleting blog posts

Changes to the tutorial's code include the following:

- Rename the template files to change the extension from .html to .html.j2 to
  make it clear that these are Jinja2 HTML files.

- Separate database interaction code from user interface code an move all
  database interaction code to flaskr/db.py.

- Revise the documentation structure.
    - Move README.md to the docs folder.
    - Move the documentation of how to use SQLite from docs/README.md to
      docs/sqlite.md.
    - Move the documentation of versions from docs/README.md to
      docs/versions.md.

## Version 0.3

This version completes the following steps of the tutorial:

- [_Blueprints and Views_](https://flask.palletsprojects.com/en/2.2.x/tutorial/views/)
- [_Templates_](https://flask.palletsprojects.com/en/2.2.x/tutorial/templates/)
- [_Static Files_](https://flask.palletsprojects.com/en/2.2.x/tutorial/static/)

This version adds the flask blueprint named `auth` for authenticating a user,
the Jinja2 HTML template files for the
[auth/login](http://127.0.0.1:5000/auth/login) and
[auth/register](http://127.0.0.1:5000/auth/register) pages, and the static CSS
file for styling the application.

Changes to the tutorial's code include the following:

- Rename the database tables from `user` to `tbl_user` and from `post` to
  `tbl_post`.

- Use an absolute import for the `flaskr.db` module.

- Revise the code for database queries to separate the individual steps.

- For the `login` function, check that the username and password fields are
  not empty.

- Rename `flask.g.db` to `flask.g.conn`, for clarity.

## Version 0.2.1

This version completes the following instructions:

- [_Define and Access the Database_](https://flask.palletsprojects.com/en/2.2.x/tutorial/database/)

This version adds the code for initializing the database.

Changes to the tutorial's code include the following:

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
