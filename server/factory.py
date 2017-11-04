# server/factory.py

from flask import Flask
from server.utils.logging_ext import setup_logger
from server.extensions import db, cache, bcrypt, cors
from server.models import User


def create_app(config='server.config.DevelopmentConfig', app=None):

    # Configure the app w.r.t Flask, databases, loggers.
    if app is None:
        app = Flask(__name__)
    app.config.from_object(config)
    setup_logger(app.config['LOGGING_LOCATION'], app.config['LOGGING_LEVEL'])
    return app


def setup_extensions(app):
    db.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)


def create_users(app):

    db.create_all()

    for user in app.config['DEFAULT_USERS']:

        found_user = User.query.filter_by(email=user['email']).first()

        if not found_user:
            new_user = User(
                email=user['email'],
                password=user['password']
            )
            # insert the user
            db.session.add(new_user)

    db.session.commit()
