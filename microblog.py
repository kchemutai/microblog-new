from flask import Flask, render_template, url_for, redirect, flash
from flask.helpers import flash
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '4fcb6ded09f29ed1452e6c53c059816a'


posts = [
    {
        'author': 'Kevin Chemutai',
        'title': 'Flask tutorial series',
        'date_posted': '25-12-2019',
        'content': 'I am revisting the flask series tutorials by corey shafer',
    },
    {
        'author': 'Jamie Verdy',
        'title': 'England in the Euros',
        'date_posted': '25-12-2021',
        'content': 'Great performance from the team, lets gooooo!!!!',
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['post', 'get'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(
            f'Account for {form.username.data} created successfully', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['post', 'get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@microblog.com' and form.password.data == 'testpass':
            flash('You have successfully logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check your email or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/reset', methods=['get', 'post'])
def reset():
    pass


if __name__ == '__main__':
    app.run(debug=True)
