# server/blueprints/api/views.py

from flask import Blueprint, make_response, jsonify
from server.utils.tokens import jwt_required
from server.utils import html_codes

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/get_data', methods=['GET'])
@jwt_required
def get_data():
    data = {'Heroes': ['Hero1', 'Hero2', 'Hero3']}
    return make_response(jsonify(data)), \
        html_codes.HTTP_OK_BASIC
