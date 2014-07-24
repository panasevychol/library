from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, EditForm, PostForm, ManageWriter, ManageTitle, SearchForm
from models import User, ROLE_USER, ROLE_ADMIN, BookTitle, BookWriter
from datetime import datetime

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
    
@app.route('/')
@app.route('/index')
def index():
    user = g.user
    titles = BookTitle.query.order_by(BookTitle.timestamp.desc())
    return render_template('index.html',
        title = 'Home',
        user = user,
        titles = titles)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out.')
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    titles = BookTitle.query.order_by(BookTitle.timestamp.desc()).filter_by(author = user)
    return render_template('user.html',
        user = user,
        titles = titles)

@app.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html',
        form = form)

@app.route('/post_book', methods = ['GET', 'POST'])
@login_required
def post_book():
    form = PostForm()
    if form.validate_on_submit():
        current_writer_name = form.book_writer.data.title()
        current_title_name = form.book_title.data.title()
        if BookWriter.query.filter_by(book_writer = current_writer_name).first() == None:
            current_writer = BookWriter(book_writer = form.book_writer.data.title())
            db.session.add(current_writer)
            flash('New writer is added.')
        else:
            current_writer = BookWriter.query.filter_by(book_writer = current_writer_name).first()

        if BookTitle.query.filter_by(book_title = current_title_name).first() == None:
            current_title = BookTitle(book_title = form.book_title.data.title(), timestamp = datetime.utcnow(), author = g.user)
            db.session.add(current_title)
            flash('Your book is posted!')
        else:
            current_title = BookTitle.query.filter_by(book_title = current_title_name).first()
            flash('This book was posted earlier.')
        current_writer.add_composed(current_title)
        db.session.add(current_writer)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('post_book.html',
        form = form)

@app.route('/manage_writers', methods = ['GET', 'POST'])
@login_required
def manage_writers():
    writers = BookWriter.query.order_by(BookWriter.book_writer.desc())
    form = ManageWriter()
    if form.validate_on_submit():
        current_writer_name = form.book_writer.data.title()
        if BookWriter.query.filter_by(book_writer = current_writer_name).first() != None:
            flash('This writer is already in Library.')
        else:
            current_writer = BookWriter(book_writer = form.book_writer.data.title())
            db.session.add(current_writer)
            db.session.commit()
            flash('Your writer is sucsessfully added!')
        return redirect(url_for('manage_writers'))


    return render_template('manage_writers.html',
        form = form,
        writers = writers)

@app.route('/edit_writer/<writer_id>', methods = ['GET', 'POST'])
@login_required
def edit_writer(writer_id):
    current_writer = BookWriter.query.filter_by(id = writer_id).first()
    form = ManageWriter()
    if form.validate_on_submit():
        if BookWriter.query.filter_by(book_writer = form.book_writer.data.title()).first() == None:
            current_writer.book_writer = form.book_writer.data.title()
            db.session.add(current_writer)
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('manage_writers'))
        else:
            flash('There is a writer with such name in Library! Please enter correct writer\'s name.')
            return redirect(url_for('manage_writers'))
    else:
        form.book_writer.data = current_writer.book_writer

    return render_template('edit_writer.html',
        form = form)

@app.route('/delete_writer/<writer_id>', methods = ['GET', 'POST'])
@login_required
def delete_writer(writer_id):
    current_writer = BookWriter.query.filter_by(id = writer_id).first()
    form = ManageWriter()
    if form.validate_on_submit():
        db.session.delete(current_writer)
        db.session.commit()
        flash('Your writer sucsessfully deleted.')
        return redirect(url_for('manage_writers'))
    else:
        form.book_writer.data = current_writer.book_writer

    return render_template('delete_writer.html',
        form = form)

@app.route('/edit_book/<book_id>', methods = ['GET', 'POST'])
@login_required
def edit_book(book_id):
    current_title = BookTitle.query.filter_by(id = book_id).first()
    form = ManageTitle()
    if form.validate_on_submit():
        current_title.book_title = form.book_title.data.title()
        db.session.add(current_title)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    else:
        form.book_title.data = current_title.book_title

    return render_template('edit_book.html',
        form = form)

@app.route('/delete_book/<book_id>', methods = ['GET', 'POST'])
@login_required
def delete_book(book_id):
    current_title = BookTitle.query.filter_by(id = book_id).first()
    form = ManageTitle()
    if form.validate_on_submit():
        db.session.delete(current_title)
        db.session.commit()
        flash('Your book sucsessfully deleted.')
        return redirect(url_for('index'))
    else:
        form.book_title.data = current_title.book_title

    return render_template('delete_book.html',
        form = form)

@app.route('/search', methods = ['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data.title(), search_by = g.search_form.search_by.data))

@app.route('/search_results/search_by_<search_by>/<query>')
@login_required
def search_results(query, search_by):
    if search_by == 'title':
        results = BookTitle.query.filter(BookTitle.book_title.contains(query)).all()
    elif search_by == 'writer':
        results = BookWriter.query.filter(BookWriter.book_writer.contains(query)).all()

    return render_template('search_results.html',
        query = query,
        results = results,
        search_by = search_by)