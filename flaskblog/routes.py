
from flask import render_template, flash, redirect, url_for, request
from flaskblog import app, bcrypt, db
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

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


@app.route('/home')
@app.route('/')
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
        db.session.commit()
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccesfull, check email or password!', 'danger')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_name)
    output_size = (128, 128)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name


@app.route('/account',  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account information has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    imgae_file = url_for(
        'static', filename='profile_pics/' + current_user.image)
    return render_template('account.html', title='Account', profile_picture=imgae_file, form=form)
