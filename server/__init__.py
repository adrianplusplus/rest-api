# server/__init__.py

import os
import logging
from flask import jsonify, make_response
from server.factory import create_app, create_users, setup_extensions
from server.utils.errors import InvalidAPIUsage
from server.utils import html_codes
from server.blueprints.auth.views import auth_blueprint

app_settings = os.getenv('FLASK_CONFIGURATION', 'server.config.DevelopmentConfig')
app = create_app(app_settings)
setup_extensions(app)
logger = logging.getLogger(__name__)

app.register_blueprint(auth_blueprint, url_prefix='/auth')


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
    create_users(app)
