from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, SelectField
from wtforms.validators import Required, Length
from app.models import User

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    
class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True

class PostForm(Form):
    book_writer = TextField('current_writer', validators = [Length(min = 1, max = 100)])
    book_title = TextField('current_title', validators = [Length(min = 1, max = 100)])

class ManageWriter(Form):
    book_writer = TextField('current_writer', validators = [Length(min = 1, max = 100)])

class ManageTitle(Form):
    book_title = TextField('current_title', validators = [Length(min = 1, max = 100)])

class SearchForm(Form):
    search = TextField('search', validators = [Required()])
    search_by = SelectField('search_by', choices=[('title', 'Title'), ('writer', 'Writer')])