# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Docstring for module."""


import os

from flask import Flask
from server.utils import setup_logger
from flask_cache import Cache


def create_cache(app):
    return Cache(app, config={'CACHE_TYPE': app.config['CACHE_TYPE']})


def create_app(config='default', app=None):

    # Configure the app w.r.t Flask, databases, loggers.
    if app is None:
        app = Flask(__name__)
    config_name = os.getenv('FLASK_CONFIGURATION', config)
    app.config.from_object(config_name)
    setup_logger(app.config['LOGGING_LOCATION'], app)
    return app


def create_user(app, db, User):

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
