from flask import request, current_app, url_for
from flask_mail import Message
from project import mail
import jwt
from functools import wraps


def token_required(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-auth')

        if not token:
            return {'msg': 'Token is missing!'}, 401

        try:
            jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return {'msg': 'Token is invalid!'}, 401

        return func(*args, **kwargs)

    return decorated


def send_activation_email(user):
    token = user.get_token()
    msg = Message('Click on the link to activate the account', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'''Please click on the following link to activate your account:
{url_for('activateuser', token=token, _external=True)}
'''
    mail.send(msg)