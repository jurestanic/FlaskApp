from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from project.config import DevConfig
from flask_mail import Mail

db = SQLAlchemy()
api = Api()
mail = Mail()


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)

    from project.users.auth import RegisterUser, ActivateUser, LoginUser
    from project.users.routes import User, AllUsers
    from project.activities.routes import Activities

    api.add_resource(RegisterUser, '/registration')
    api.add_resource(LoginUser, '/login')
    api.add_resource(AllUsers, '/index')
    api.add_resource(ActivateUser, '/user/activate/<token>')
    api.add_resource(User, '/user')
    api.add_resource(Activities, '/activities')

    api.init_app(app)

    with app.app_context():
        db.create_all()

    return app
