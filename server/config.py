# server/config.py

import os
import logging


class BaseConfig(object):
    """Base configuration."""
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    JWT_MAX_AGE = 60 * 30
    CACHE_TIMEOUT = 60 * 30
    CACHE_TYPE = 'simple'
    JWT_REVOCATION = '/auth/logout'
    SECRET_KEY = os.getenv('SECRET_KEY', 'Secret')
    DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_FORMAT = "[%(asctime)s] [%(funcName)-30s] +\
                                    [%(levelname)-6s] %(message)s"
    LOGGING_LOCATION = 'log/'
    LOGGING_LEVEL = logging.INFO
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml',
                          'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DEFAULT_USERS = [
        {
            'email': 'test@tourister.com',
            'password': 'TestTourister2017@'
        }
    ]


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BaseConfig.BASEDIR, 'dev.sqlite')
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    JWT_MAX_AGE = 2
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    LOGGING_LEVEL = logging.DEBUG


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BaseConfig.BASEDIR, 'prod.sqlite')
