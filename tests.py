from project.config import TestConfig
from project import create_app, db
import unittest
import jwt


app = create_app(TestConfig)


class CreateUser(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.email = "test@test.com"
        self.user_name = "testimir"
        self.token = jwt.encode({'user_id': 17}, app.config['SECRET_KEY'])

    def post_user(self):
        return self.client.post(
            '/user',
            data=dict(first_name="Testimir",
                      last_name="Testović",
                      user_name= self.user_name,
                      email= self.email,
                      password="test123"),
            headers={'x-auth': self.token}
        )

    def test_invalid_token(self):
        self.token = 'invalid-token'

        res = self.post_user()

        self.assertEqual(res.status_code, 401)

    def test_email_exists(self):
        self.post_user()

        res = self.post_user()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data, b'{"msg": "User with given email already exists!"}\n')

    def test_username_exists(self):
        self.post_user()

        self.email = 'different@mail.com'
        res = self.post_user()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data, b'{"msg": "User with given username already exists!"}\n')

    def test_user_created(self):
        res = self.post_user()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data, b'{"msg": "Please check mail to activate the account"}\n')


class UpdateUser(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.old_password = "test123"
        self.new_password = "pitajtest"
        self.confirm_password = "pitajtest"
        self.token = jwt.encode({'user_id': 1}, app.config['SECRET_KEY'])

        self.client.post(
            '/user',
            data=dict(first_name="Testimir",
                      last_name="Testović",
                      user_name="testimir",
                      email="test@test.com",
                      password=self.old_password),
            headers={'x-auth': self.token}
        )

    def update_user(self):
        return self.client.put(
                '/user',
                data=dict(first_name="Testimir",
                          last_name="Testović",
                          old_password=self.old_password,
                          new_password=self.new_password,
                          confirm_password=self.confirm_password),
                headers={'x-auth': self.token}
            )

    def test_invalid_token(self):
        token = 'invalid-token'

        res = self.client.put(f'/user', headers={'x-auth': token})

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data, b'{"msg": "Token is invalid!"}\n')


    def test_incorrect_password(self):
        self.old_password = "invalid123"

        res = self.update_user()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data, b'{"msg": "Password is incorrect!"}\n')

    def test_non_matching_passwords(self):
        self.confirm_password = "uvikkontra"

        res = self.update_user()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data, b'{"msg": "Passwords don\'t match"}\n')

    def test_successful_change(self):

        res = self.update_user()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'{"msg": "You successfully changed your password"}\n')


class ActivateUser(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.token = jwt.encode({'user_id': 1}, app.config['SECRET_KEY'])

        self.client.post(
            '/user',
            data=dict(first_name="Testimir",
                      last_name="Testović",
                      user_name="Test",
                      email="test@test.com",
                      password="test123"),
            headers={'x-auth': self.token}
        )

    def test_invalid_token(self):
        token = 'invalid-token'

        res = self.client.put(f'/user/activate/{token}')

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data, b'{"msg": "Token is invalid!"}\n')

    def test_activation(self):
        res = self.client.put(f'/user/activate/{self.token.decode("utf-8")}')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'{"msg": "You successfuly activated your account!"}\n')


class DeactivateUser(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.token = jwt.encode({'user_id': 1}, app.config['SECRET_KEY'])
        self._id = 1

        self.client.post(
            '/user',
            data=dict(first_name="Testimir",
                      last_name="Testović",
                      user_name="Test",
                      email="test@test.com",
                      password="test123"),
            headers={'x-auth': self.token}
        )

    def test_if_no_user(self):
        self._id = 2

        res = self.client.delete(f'/user?id={self._id}',  headers={'x-auth': self.token})

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data, b'{"msg": "There is no user with ID:2!"}\n')

    def test_deactivate(self):
        res = self.client.delete(f'/user?id={self._id}',  headers={'x-auth': self.token})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'{"msg": "User with ID:1 successfully deactivated!"}\n')


if __name__ == '__main__':
    unittest.main()

