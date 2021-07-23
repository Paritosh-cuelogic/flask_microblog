from flask import render_template, current_app
from app.mail import send_mail


def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_mail(
        subject='[Microblog] password reset',
        sender=current_app.config['ADMINS'][0],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token),
        recipients=[user.email]
    )