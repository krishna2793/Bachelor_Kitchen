from configparser import ConfigParser
from datetime import timedelta


class ProdConfig(object):
    config = ConfigParser()
    config.read('../config.ini')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
        config.get('rds', 'user'),
        config.get('rds', 'password'),
        config.get('rds', 'host'),
        config.get('rds', 'port'),
        config.get('rds', 'database')
    )
    SECRET_KEY = config.get('key', 'secret_key')
    MAIL_USERNAME = config.get('mail', 'username')
    MAIL_PASSWORD = config.get('mail', 'password')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
