import json
import server.models as models
import server.marshmallow_schemas as schemas
from flask import Blueprint, make_response, jsonify
from flask_restful import Resource, Api
from server.utils.tokens import jwt_required

class Tourister(Resource):
    
    decorators = [jwt_required] 

    def get(self, id):
        return "returns one Turister with id :" + id

    def delete(self, id):
        return "deletes a tourister with id :" + id

    def put(self, id):
        return "updates a tourister with id :" + id

class TouristerList(Resource):
    
    decorators = [jwt_required]

    def get(self):
        return "returns all touristers"

    def post(self):
        return "creates a new turister"