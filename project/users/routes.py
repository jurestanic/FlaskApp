from flask_restful import Resource, reqparse
from project.models import UserModel
from project.utils import send_activation_email
from project.utils import token_required
from flask import request, current_app


class User(Resource):

    @staticmethod
    def get_update_args():
        parser = reqparse.RequestParser()

        parser.add_argument('first_name', type=str, required=True, help="First name is required!")
        parser.add_argument('last_name', type=str, required=True, help="Last name is required!")
        parser.add_argument('old_password', type=str, required=True, help="Old password is required!")
        parser.add_argument('new_password', type=str, required=True, help="New password is required!")
        parser.add_argument('confirm_password', type=str, required=True, help="Confirm password is required!")

        return parser.parse_args()

    @token_required
    def put(self):

        data = User.get_update_args()

        token = request.headers.get('x-auth')
        user = UserModel.verify_token(token)

        if not user.check_password(data['old_password']):
            return {'msg': 'Password is incorrect!'}, 400

        if data['new_password'] != data['confirm_password']:
            return {'msg': 'Passwords don\'t match'}, 400

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.password = user.hash_password(data['new_password'])
        user.save_to_db()

        return {'msg': 'You successfully changed your password'}, 200

    @staticmethod
    def get_create_args():
        parser = reqparse.RequestParser()

        parser.add_argument('first_name', type=str, required=True, help="First name is required!")
        parser.add_argument('last_name', type=str, required=True, help="Last name is required!")
        parser.add_argument('user_name', type=str, required=True, help="Username is required!")
        parser.add_argument('email', type=str, required=True, help="Email is required!")
        parser.add_argument('password', type=str, required=True, help="Password is required!")

        return parser.parse_args()

    @token_required
    def post(self):

        data = User.get_create_args()

        user = UserModel.find_by_email(data['email'])
        if user:
            return {'msg': 'User with given email already exists!'}, 400

        user = UserModel.find_by_username(data['user_name'])
        if user:
            return {'msg': 'User with given username already exists!'}, 400

        user = UserModel(**data)
        user.save_to_db()

        if not current_app.config['TESTING']:
            send_activation_email(user)

        return {'msg': 'Please check mail to activate the account'}, 201

    @token_required
    def delete(self):
        _id = request.args.get('id')
        user = UserModel.find_by_id(_id)

        if user is None:
            return {'msg': f"There is no user with ID:{_id}!"}, 404

        user.set_status(0)

        return {'msg': f"User with ID:{_id} successfully deactivated!"}


class AllUsers(Resource):

    def get(self):

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 2, type=int)

        search_key = request.args.get('search', type=str)
        search_val = request.args.get('val', type=str)

        if search_key == 'password':
            return {'error': "You can't search by password! "}, 400

        kwargs = {search_key: search_val}

        if search_key:
            users = UserModel.query.filter_by(**kwargs).paginate(page=page, per_page=page_size)
        else:
            users = UserModel.query.paginate(page=page, per_page=page_size)

        return {'users': [user.json() for user in users.items]}





