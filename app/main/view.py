import datetime
from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_required
from app.main.forms import PostForm
from app import db
from app.post.models import Post
from app.main import main_blueprint


@main_blueprint.before_request
def before_request():
    """ Check if user is authenticated and if yes then store current time as last seen """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()


@main_blueprint.route('/index', methods=['GET', 'POST'])
@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """ Allow login user to add new post and also show all the posts added by following users """
    posts = current_user.followed_posts().all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post submitted successfully')
        return redirect(url_for('main.index'))
    return render_template('index.html', title='Home', posts=posts, form=form)


@main_blueprint.route('/explore')
def explore():
    """ Allow users to see all the posts """
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts)