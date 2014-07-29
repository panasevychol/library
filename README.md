Library
=======

<h3>Library application on Flask</h3>

This is the simple application to rule electronic library.

Technologies that have been used to realize:
  - Flask
  - SQLAlchemy
  - SQLite
  - Jinja2 Templates
  - WTForms
  - jQuery

Key features:
- Sign In with OpenID
- ability to add/edit/remove book
- ability to manage writers (add/edit/remove)
- search by the name of writer or book title
- user info editor
- minimalistic GUI

Script add_test_data.py adds a user and a few books posted by that user to fill the application with some data.<br>
Also repository contains database created with script db_create.py. I signed in once with my OpenID to post a few books to make Library not empty at all.<br>
Repository does not contain installed Flask environment and required expansions.<br>
run.py runs the application indebug mode.<br>
<br>
Deployed application:<br>
http://library-panasevychol.herokuapp.com/
