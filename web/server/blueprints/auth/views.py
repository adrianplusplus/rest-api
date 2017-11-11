# server/blueprints/auth/views.py

from flask import Blueprint, request, make_response, jsonify, \
    current_app as app
from server.extensions import bcrypt, db
from server.models import User, BlacklistToken
from server.utils.tokens import jwt_required, encode_auth_token
from server.utils import html_codes
from server.utils.errors import InvalidAPIUsage

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route("/register", methods=['POST'])
def register():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        user = User(
            email=post_data.get('email'),
            password=post_data.get('password')
        )
        # insert the user
        db.session.add(user)
        db.session.commit()
        # generate the auth token
        auth_token = encode_auth_token(user.id, user.admin)
        responseObject = {
            'status': 'success',
            'message': 'Successfully registered.',
            'auth_token': auth_token.decode(),
            'token_max_age': app.config.get('JWT_MAX_AGE')
        }
        return make_response(jsonify(responseObject)), \
            html_codes.HTTP_OK_CREATED
    else:
        raise InvalidAPIUsage(
            message='User already exists. Please Log in.',
            status_code=html_codes.HTTP_BAD_FORBIDDEN
        )


@auth_blueprint.route("/login", methods=['POST'])
def login():
    # get the post data
    post_data = request.get_json()
    # fetch the user data
    user = User.query.filter_by(
        email=post_data.get('email')
    ).first()
    if user and bcrypt.check_password_hash(
        user.password, post_data.get('password')
    ):
        auth_token = encode_auth_token(user.id, user.admin)
        responseObject = {
            'status': 'success',
            'message': 'Successfully logged in.',
            'auth_token': auth_token.decode(),
            'token_max_age': app.config.get('JWT_MAX_AGE')
        }
        return make_response(jsonify(responseObject)), \
            html_codes.HTTP_OK_BASIC
    else:
        raise InvalidAPIUsage(
            message='User does not exist.',
            status_code=html_codes.HTTP_BAD_NOTFOUND
        )


@auth_blueprint.route("/logout", methods=['POST'])
@jwt_required
def logout():
    auth_token = request.headers.get('Authentication-Token').split(" ")[1]
    blacklist_token = BlacklistToken(token=auth_token)
    # insert the token
    db.session.add(blacklist_token)
    db.session.commit()
    responseObject = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return make_response(jsonify(responseObject)), \
        html_codes.HTTP_OK_BASIC
