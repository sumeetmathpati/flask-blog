
from flask import render_template, flash, redirect, url_for
from flaskblog import app, bcrypt, db
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user


posts = [
    {
        'author': 'Sumeet M',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'Jan 28, 2000'
    },
    {
        'author': 'John Doe',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'Jan 29, 2000'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 3',
        'content': 'Third Post Content',
        'date_posted': 'Jan 30, 2000'
    }
]


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', posts=posts, title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.commit()
        flash(f'Your account has been created, you are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccesfull, check email or password!', 'danger')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
