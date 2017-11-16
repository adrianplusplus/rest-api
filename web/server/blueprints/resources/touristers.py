import json
import server.models as models
import server.marshmallow_schemas as schemas
from server.utils import errors, html_codes
from flask import Blueprint, make_response, jsonify
from flask_restful import Resource, Api
from server.core import tokens

schema = schemas.TouristerSchema()

class Tourister(Resource):
    
    decorators = [tokens.jwt_required] 

    def get(self, id):
        tourister = models.Tourister.query.get(id)
        if not tourister:
            return {}, html_codes.HTTP_BAD_NOTFOUND
        response = json.loads(schema.dumps(tourister).data)
        return jsonify(tourister=tourister)

    def delete(self, id):
        return "deletes a tourister with id :" + id

    def put(self, id):
        return "updates a tourister with id :" + id

class TouristerList(Resource):
    
    decorators = [tokens.jwt_required] 

    def get(self):
        touristers = models.Tourister.query.all()
        if not touristers:
            return {}, html_codes.HTTP_BAD_NOTFOUND
        response = [json.loads(schema.dumps(t).data) for t in touristers]
        return jsonify(touristers = response)

    def post(self):
        return "creates a new turister"