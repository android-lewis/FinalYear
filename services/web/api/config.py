import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/api/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/api/images"
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "abstract.styler@gmail.com"
    MAIL_PASSWORD = "9FvVs4xW!!"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class TestConfig(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/api/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/api/images"
    SECRET_KEY = os.getenv('SECRET_KEY')