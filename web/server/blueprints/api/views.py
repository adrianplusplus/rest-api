# server/blueprints/api/views.py

from flask import Blueprint, make_response, jsonify, request
from flask_restful import  Api
from server.utils import errors, html_codes
from server.core import tokens
from server.blueprints.resources import touristers, services

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


@api_blueprint.route('/get_data', methods=['GET'])
@tokens.jwt_required
def get_data():
    data = {'Heroes': ['Hero1', 'Hero2', 'Hero3']}
    return make_response(jsonify(data)), \
        html_codes.HTTP_OK_BASIC


@api_blueprint.route('/get_data_non_json', methods=['GET'])
@tokens.jwt_required
def get_data_non_json():
    return make_response("Non JSON data!",
                         html_codes.HTTP_OK_BASIC)


@api_blueprint.route('/protected_get_data', methods=['GET'])
@tokens.jwt_required
def protected_get_data():
    # get auth token
    auth_token = request.headers.get('Authentication-Token').split(" ")[1]
    token_data = tokens.decode_auth_token(auth_token)
    if not token_data['is_admin']:
        raise errors.InvalidAPIUsage(
            message='Permission denied.',
            status_code=html_codes.HTTP_BAD_FORBIDDEN
        )
    data = {'Heroes': ['Hero1', 'Hero2', 'Hero3']}
    return make_response(jsonify(data), html_codes.HTTP_OK_BASIC)


api.add_resource(touristers.Tourister, '/touristers/<id>')
api.add_resource(touristers.TouristerList, '/touristers')
api.add_resource(services.Service, '/services/<id>')
api.add_resource(services.ServiceList, '/services') 