from app import db, app

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    book_titles = db.relationship('BookTitle', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def seen_book_writers(self):
        return BookWriter.query.order_by(BookWriter.book_writer.desc())

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    def __repr__(self):
        return '<User %r>' % (self.nickname)    
        


composition = db.Table('composition',
    db.Column('composer_id', db.Integer, db.ForeignKey('book_writer.id')),
    db.Column('composed_id', db.Integer, db.ForeignKey('book_title.id'))
)

class BookWriter(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_writer = db.Column(db.String(140))
    compositions = db.relationship('BookTitle',
        secondary = composition,
        backref = db.backref('composers', lazy = 'dynamic'),     
        lazy = 'dynamic',
        cascade = 'all,delete'
        )

    def add_composed(self, book_title):
        if not self.is_added(book_title):
            self.compositions.append(book_title)
            return self

    def delete_composed(self, book_title):
        if self.is_added(book_title):
            self.compositions.remove(book_title)
            return self

    def delete_all_composed(self):
        all_to_delete = self.compositions.filter(composition.c.composer_id == self.id)
        print all_to_delete
        return self


    def is_added(self, book_title):
        return self.compositions.filter(composition.c.composed_id == book_title.id).count() > 0


    def __repr__(self):
        return '<BookWriter %r>' % (self.book_writer)

class BookTitle(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    book_title = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<BookTitle %r>' % (self.book_title)
        