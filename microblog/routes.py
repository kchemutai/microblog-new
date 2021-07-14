import os
import secrets
from flask import render_template, url_for, redirect, flash, request
from wtforms.validators import Email
from microblog.forms import LoginForm, PostForm, RegistrationForm, UpdateAccountForm
from microblog.models import User, Post
from microblog import app, bicrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['post', 'get'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bicrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Account for {form.username.data} created successfully, You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bicrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check your username or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/reset', methods=['get', 'post'])
def reset():
    pass


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, picture_extension = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + picture_extension
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics/' + picture_file_name)

    # resize the image
    image_output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(image_output_size)
    i.save(picture_path)
    return picture_file_name


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            pic = save_picture(form.picture.data)
            current_user.image_file = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account details have been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/post/new', methods=['POSt', 'GET'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has successfully been submitted')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post', form=form)