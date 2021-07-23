from flask import render_template, redirect, flash, url_for, request, Response
from flask_login import login_required, current_user
from app import db

from app.auth.models import BlogUser
from app.post import post_blueprint
from app.post.forms import EditProfileForm, EmptyForm


@post_blueprint.route('/user/<username>')
@login_required
def user(username):
    """ Allow user to see other users profile """
    form = EmptyForm()
    user = BlogUser.query.filter_by(username=username).first_or_404()
    posts = []
    user_posts = user.posts.all()
    if  user_posts is not None:
        for post in user_posts:
            posts.append({
                'author': user,
                'body': post.body
            })
    return render_template('user.html', user=user, posts=posts, form=form)


@post_blueprint.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """ Allow login user to update own profile """
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('post.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@post_blueprint.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    user = BlogUser.query.filter_by(username=username).first()
    current_user.follow(user)
    db.session.commit()
    flash('You started following to ' + username)
    return redirect(url_for('post.user', username=username))


@post_blueprint.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user = BlogUser.query.filter_by(username=username).first()
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You unfollow {username}')
    return redirect(url_for('post.user', username=username))
