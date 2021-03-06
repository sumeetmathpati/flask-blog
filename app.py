from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '1327cc612108218c85d429a7a288c145'

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
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Register ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccesfull, check email or password!', 'danger')
    return render_template('login.html', form=form, title='Login')
