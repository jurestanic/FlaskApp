import os


class DevConfig:

    db_username = os.environ['PROJECT_DB_USERNAME']
    db_password = os.environ['PROJECT_DB_PASSWORD']
    db_name = os.environ['PROJECT_DB_NAME']

    mail_username = os.environ['PROJECT_MAIL_USERNAME']
    mail_password = os.environ['PROJECT_MAIL_PASSWORD']

    SECRET_KEY = os.environ['PROJECT_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_username}:{db_password}@localhost/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = mail_username
    MAIL_PASSWORD = mail_password


class TestConfig:

    db_username = os.environ['TEST_PROJECT_DB_USERNAME']
    db_password = os.environ['TEST_PROJECT_DB_PASSWORD']
    db_name = os.environ['TEST_PROJECT_DB_NAME']

    TESTING = True
    SECRET_KEY = os.environ['PROJECT_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_username}:{db_password}@localhost/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False





