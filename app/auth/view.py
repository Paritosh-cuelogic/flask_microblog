from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user

from app import db
from app.auth import ab

from app.auth.forms import LoginForm, RegisterUserForm, PasswordReset, ResetPasswordForm


from app.auth.models import BlogUser
from app.auth.email import send_password_reset_email


@ab.route('/login', methods=['GET', 'POST'])
def login():
    """
        Allow user to login into the system by providing valid username and password.
        If user already login then redirect user to home page
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = BlogUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f'Invalid username or password')
            return redirect(url_for('loginauth.login'))
        login_user(user, remember=form.remember_me.data)
        next_route = request.args.get('next')
        if not next_route:
            next_route = url_for('main.index')
        return redirect(next_route)
    return render_template('login.html', form=form)


@ab.route('/logout')
def logout():
    """ Logout user from the system """
    logout_user()
    flash("Logout successfully")
    return redirect(url_for('loginauth.login'))


@ab.route('/register', methods=['GET', 'POST'])
def register():
    """
        Register new user into the system.
        If user already login then redirect user to home page
    """
    form = RegisterUserForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        user = BlogUser(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully')
        return redirect(url_for('loginauth.login'))
    return render_template('register.html', form=form)


@ab.route('/forgot_password', methods=['GET', 'POST'])
def reset_password_request():
    """ Send reset password link to entered main address """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = PasswordReset()
    if form.validate_on_submit():
        user = BlogUser.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for reset password link')
        return redirect(url_for('loginauth.login'))
    return render_template('reset_password_request.html', form=form)


@ab.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """ Accept and update new password """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = BlogUser.verify_reset_password(token)
    if not user:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Password reset successfully')
        return redirect(url_for('loginauth.login'))
    return render_template('reset_password.html', form=form)
