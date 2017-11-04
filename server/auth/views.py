# flask_app/auth/views.py
# Uses https://github.com/realpython/flask-jwt-auth/ as reference.

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from server import bcrypt, db, app
from server.models import User, BlacklistToken
from server.utils.tokens import jwt_required, encode_auth_token
from server.utils import html_codes
from server.utils import InvalidAPIUsage

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
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
            auth_token = encode_auth_token(user.id)
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


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # fetch the user data
        user = User.query.filter_by(
            email=post_data.get('email')
        ).first()
        if user and bcrypt.check_password_hash(
            user.password, post_data.get('password')
        ):
            auth_token = encode_auth_token(user.id)
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


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    @jwt_required
    def post(self):
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


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    app.config.get('JWT_REVOCATION'),
    view_func=logout_view,
    methods=['POST']
)
