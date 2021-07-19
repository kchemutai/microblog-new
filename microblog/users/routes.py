from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from microblog.models import User, Post
from microblog import bicrypt, db
from microblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, PasswordResetRequestForm, PasswordResetForm
from microblog.users.utils import save_picture, send_reset_email


users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/register', methods=['post', 'get'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
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
        return redirect(url_for('users_bp.login'))
    return render_template('register.html', form=form)


@users_bp.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bicrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main_bp.home'))
        else:
            flash('Login unsuccessful, please check your username or password', 'danger')
    return render_template('login.html', form=form)


@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_bp.home'))


@users_bp.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users_bp.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users_bp.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) .order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)


@users_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to your email with instructions to reset your passowrd', 'info')
        return redirect(url_for('users_bp.login'))
    return render_template('reset_password_request.html', form=form)


@users_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or Expired token', 'warning')
        return redirect(url_for('users_bp.reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bicrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('You password was succefully changed', 'success')
        return redirect(url_for('users_bp.login'))
    return render_template('reset_password.html', form=form)
