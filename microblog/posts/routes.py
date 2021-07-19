
from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from microblog.models import User, Post
from microblog import db
from microblog.posts.forms import PostForm

posts_bp = Blueprint('posts_bp', __name__)


@posts_bp.route('/post/new', methods=['POST', 'GET'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has successfully been submitted', 'success')
        return redirect(url_for('main_bp.home'))
    return render_template('new_post.html', title='New Post', form=form, legend='Create Post')


@posts_bp.route('/post/<int:post_id>', methods=['post', 'get'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts_bp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():

        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts_bp.view_post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('new_post.html', title='Update Post', legend='Update Post', form=form)


@posts_bp.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('main_bp.home'))
