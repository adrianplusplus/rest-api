"""Implicit module which returns token-expiry time from Flask-security."""
import datetime
import jwt
import json
import logging
from flask import jsonify, request, make_response, after_this_request
from server import app
from server.models import BlacklistToken
from server.utils import html_codes

logger = logging.getLogger(__name__)


def jwt_required(func):
    def func_wrapper(*args, **kwargs):

        # get the auth token
        auth_header = request.headers.get('Authentication-Token')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = None

        if auth_token:
            # resp is user id in case of sucess
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                if (request.path != app.config.get('JWT_REVOCATION')):
                    after_this_request(
                        extend_jwt(resp, auth_token),
                    )
                return func(*args, **kwargs)
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), \
                html_codes.HTTP_BAD_UNAUTHORIZED
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), \
                html_codes.HTTP_BAD_FORBIDDEN

    func_wrapper.__name__ = func.__name__
    return func_wrapper


def extend_jwt(user_id, token_to_revoke):
    def decorator(response):
        auth_token = encode_auth_token(user_id)
        if (response.content_type == "application/json"):
            data = json.loads(response.get_data().decode())
            if (isinstance(data, dict)):
                data['auth_token'] = auth_token.decode()
                data['token_max_age'] = app.config.get('JWT_MAX_AGE')
                response.set_data(json.dumps(data))
            # blacklist_token = BlacklistToken(token=token_to_revoke)
            # db.session.add(blacklist_token)
            # db.session.commit()
        return response
    return decorator


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(
                days=0,
                seconds=app.config.get('JWT_MAX_AGE')),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return str(e)


def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        is_blacklisted_token = check_blacklist(auth_token)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def check_blacklist(auth_token):
    """
    Check whether auth token has been blacklisted
    :param auth_token:
    :return: bool
    """
    res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
    if res:
        return True
    else:
        return False
