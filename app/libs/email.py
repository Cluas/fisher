from threading import Thread
from flask_mail import Message
from flask import current_app, render_template

from app import mail


def send_mail(to, subject, template, **kwargs):
    subject_prefix = current_app.config.get('MAIL_SUBJECT_PREFIX')
    sender = current_app.config.get('MAIL_SENDER')
    msg = Message(subject_prefix + subject, sender=sender, recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=async_send_mail, args=[current_app, msg])
    thread.start()
    return thread


def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)
