import os

class config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '\x07}\xe7Y0mH\xbe\x0f\x0e\x93\x82\xfaX$\xa8P\xab\x95\xb2U\xce\xddf'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///registered.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'kiwanisfutbol@gmail.com'
    MAIL_PASSWORD = 'ugctghcebxdnbiyx'

class ProductionConfig(config):
    pass

class DevelopmentConfig(config):
    DEBUG = True

class TestingConfig(config):
    TESTING = True
