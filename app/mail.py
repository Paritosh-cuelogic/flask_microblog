from threading import Thread
from flask import current_app
from flask_mail import Message
from app import flask_mail


def send_async_mail(application, msg):
    with application.app_context():
        flask_mail.send(msg)


def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    # msg.body = text_body
    msg.html = html_body
    # flask_mail.send(msg)
    Thread(target=send_async_mail, args=(current_app._get_current_object(), msg)).start()
