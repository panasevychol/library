import os

from config import basedir
from app import app, db
from app.models import User, BookWriter, BookTitle
from datetime import datetime

u = User(nickname = 'Petro', email = 'petro@email.com')
w1 = BookWriter(book_writer = 'Joan Rowling')
db.session.add(w1)
t1 = BookTitle(book_title = 'Harry Potter And The Philosopher Stone', timestamp = datetime.utcnow(), author = u)
w1.add_composed(t1)
db.session.add(w1)
db.session.commit()
t1 = BookTitle(book_title = 'Harry Potter And The Chamber Of Secrets', timestamp = datetime.utcnow(), author = u)
w1.add_composed(t1)
db.session.add(w1)
db.session.commit()
t1 = BookTitle(book_title = 'Harry Potter And The Prisoner Of Azkaban', timestamp = datetime.utcnow(), author = u)
w1.add_composed(t1)
db.session.add(w1)
db.session.commit()
t1 = BookTitle(book_title = 'Harry Potter And The Goblet Of Fire', timestamp = datetime.utcnow(), author = u)
w1.add_composed(t1)
db.session.add(w1)
db.session.commit()
t1 = BookTitle(book_title = 'Harry Potter And The Order Of Phoenix', timestamp = datetime.utcnow(), author = u)
w1.add_composed(t1)
db.session.add(w1)
db.session.commit()
t1 = BookTitle(book_title = 'Harry Potter And The Half-Blood Prince', timestamp = datetime.utcnow(), author = u)
w1.add_composed(t1)
db.session.add(w1)
db.session.commit()
t1 = BookTitle(book_title = 'Harry Potter And The Deadly Hallows', timestamp = datetime.utcnow(), author = u)
w1.add_composed(t1)
db.session.add(w1)
db.session.commit()