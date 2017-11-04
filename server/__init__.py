# server/__init__.py

import os
import logging

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# auth
from flask import jsonify, make_response
from server.factory import create_app, create_user, create_cache
from flask_cors import CORS
from server.utils import InvalidAPIUsage
from server.utils import html_codes


app = Flask(
    __name__,
    static_folder='./static'
)


app_settings = os.getenv('APP_SETTINGS', 'server.config.DevelopmentConfig')
app.config.from_object(app_settings)


bcrypt = Bcrypt(app)
cache = create_cache(app)
db = SQLAlchemy(app)
cors = CORS(app)
logger = logging.getLogger(__name__)


from server.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)


from server.models import User


@app.errorhandler(Exception)
def handle_errors(error):
    if isinstance(error, InvalidAPIUsage):
        error_dict = error.to_dict()
        status_code = error.status_code
        logger.error(error_dict['message'])
    else:
        error_dict = dict()
        error_dict['message'] = 'Some error occurred. Please try again.'
        status_code = html_codes.HTTP_SERVER_ERROR
        logger.error(str(error))
    error_dict['status'] = 'fail'
    return make_response(jsonify(error_dict)), \
        status_code


@app.route('/')
def index():
    return 'App is running!'


@app.before_first_request
def init():
    create_user(app, db, User)
