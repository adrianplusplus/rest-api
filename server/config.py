# server/config.py

import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))

CONFIG = {
    "development": "server.config.DevelopmentConfig",
    "stage": "server.config.StageConfig",
    "testing": "server.config.TestingConfig",
    "production": "server.config.ProductionConfig",
    "default": "server.config.DevelopmentConfig"
}


class BaseConfig(object):
    """Base configuration."""
    JWT_MAX_AGE = 60 * 30
    CACHE_TIMEOUT = 60 * 30
    CACHE_TYPE = 'simple'
    JWT_REVOCATION = '/auth/logout'
    SECRET_KEY = os.getenv('SECRET_KEY', 'Secret')
    DEBUG = False
    TESTING = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_FORMAT = "[%(asctime)s] [%(funcName)-30s] +\
                                    [%(levelname)-6s] %(message)s"
    LOGGING_LOCATION = 'log/'
    LOGGING_LEVEL = logging.INFO
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml',
                          'application/json', 'application/javascript']
    WTF_CSRF_ENABLED = False
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    USERS = [
        {
            'EMAIL': 'test@qti.qualcomm.com',
            'PASS': 'TestCNS2016@'
        }
    ]


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    DEBUG_TB_ENABLED = True
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    JWT_MAX_AGE = 2
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    DEBUG_TB_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class StageConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'Secret')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
    DEBUG_TB_ENABLED = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'Secret')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
    DEBUG_TB_ENABLED = False
