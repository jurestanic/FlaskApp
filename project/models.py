from project import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask import current_app
import jwt


class UserModel(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(55), nullable=False)
    last_name = db.Column(db.String(55), nullable=False)
    user_name = db.Column(db.String(55), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer)
    activity = db.relationship('ActivityModel', backref='user', lazy=True)

    def __init__(self, first_name, last_name, user_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.email = email
        self.password = self.hash_password(password)
        self.status = 0

    def get_token(self):
        token = jwt.encode({'user_id': self.id}, current_app.config['SECRET_KEY'])
        return token

    @classmethod
    def verify_token(cls, token):

        if not token:
            return {'msg': 'Token is missing!'}, 401

        try:
            user = jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return {'msg': 'Token is invalid!'}, 401

        return cls.find_by_id(user['user_id'])

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(user_name=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_status(self, status):
        self.status = status
        db.session.commit()

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def json(self):
        return {'username': self.user_name}

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.user_name}', '{self.last_name}')"


class ActivityModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    route_name = db.Column(db.String(55), nullable=False)
    request_time = db.Column(db.Float, nullable=False)

    def __init__(self, user_id, route_name, request_time):
        self.user_id = user_id
        self.route_name = route_name
        self.request_time = request_time

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
                'username': self.user.first_name,
                'created_at': str(self.created_at),
                'route_name': self.route_name,
                'request_time': self.request_time
                }

    def __repr__(self):
        return f"User('{self.user}', '{self.route_name}', '{self.request_time}')"


