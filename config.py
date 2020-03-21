import os

class config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///registered.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'kiwanisfutbol@gmail.com'
    MAIL_PASSWORD = 'ugctghcebxdnbiyx'

class ProductionConfig(config):
    DEBUG = True

class DevelopmentConfig(config):
    DEBUG = True

class TestingConfig(config):
    TESTING = True
