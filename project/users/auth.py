from flask_restful import Resource, reqparse
from flask import url_for
from project.models import UserModel, ActivityModel
from project.utils import send_activation_email
import time


class RegisterUser(Resource):

    @staticmethod
    def get_register_args():
        parser = reqparse.RequestParser()

        parser.add_argument('first_name', type=str, required=True, help="First name is required!")
        parser.add_argument('last_name', type=str, required=True, help="Last name is required!")
        parser.add_argument('user_name', type=str, required=True, help="Username is required!")
        parser.add_argument('email', type=str, required=True, help="Email is required!")
        parser.add_argument('password', type=str, required=True, help="Password is required!")

        return parser.parse_args()

    def post(self):

        data = RegisterUser.get_register_args()

        user = UserModel.find_by_email(data['email'])
        if user:
            return {'msg': 'User with given email already exists!'}, 400

        user = UserModel.find_by_username(data['user_name'])
        if user:
            return {'msg': 'User with given username already exists!'}, 400

        user = UserModel(**data)
        user.save_to_db()

        send_activation_email(user)

        return {'msg': 'Please check mail to activate the account'}, 201


class LoginUser(Resource):

    @staticmethod
    def get_login_args():
        parser = reqparse.RequestParser()

        parser.add_argument('user_name', type=str, required=True, help="Username is required!")
        parser.add_argument('password', type=str, required=True, help="Password is required!")

        return parser.parse_args()

    # OVDJE SAM STAVIO POST METODU UMJESTO TRAŽENE GET, JER BI INAČE TREBAO STAVLJATI PASSWORD U QUERY STRING

    def post(self):
        start_time = time.time()

        data = LoginUser.get_login_args()

        user = UserModel.find_by_username(data['user_name'])

        if not user:
            return {'error': 'No user with given username'}, 400

        if user.status == 0:
            return {'error': 'You must activate your account'}, 400

        if not user.check_password(data['password']):
            return {'error': 'Password is incorrect'}, 400

        token = user.get_token()

        log = ActivityModel(user.id, url_for('loginuser'), (time.time() - start_time))
        log.save_to_db()

        return {'token': token.decode('utf-8')}


class ActivateUser(Resource):

    def put(self, token):
        user = UserModel.verify_token(token)

        if not isinstance(user, UserModel):
            return user

        user.set_status(1)
        return {'msg': 'You successfuly activated your account!'}, 200
