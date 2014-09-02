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
run.py runs the application in debug mode.<br>
<br>
Deployed application:<br>
http://library-panasevychol.herokuapp.com/
<br><br>
Required installations to run app from computer (on Windows):
  - install <a href='www.python.org/download/'>Python 2.7</a>
  - execute following list of commands to install all required packages:<br><br><i>
    flask\Scripts\pip install flask==0.9<br>
    flask\Scripts\pip install flask-login<br>
    flask\Scripts\pip install flask-openid<br>
    flask\Scripts\pip install sqlalchemy==0.7.9<br>
    flask\Scripts\pip install flask-sqlalchemy==0.16<br>
    flask\Scripts\pip install sqlalchemy-migrate==0.7.2<br>
    flask\Scripts\pip install flask-whooshalchemy==0.55a<br>
    flask\Scripts\pip install flask-wtf==0.8.4<br>
    flask\Scripts\pip install pytz==2013b<br>
    flask\Scripts\pip install flask-babel==0.8<br>
    flask\Scripts\pip install flup</i>

  - create Virtual environment: install virtualenv ('pip install virtualenv') and execute 'virtualenv flask' to set it up

