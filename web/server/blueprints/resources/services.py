import json
import server.models as models
import server.marshmallow_schemas as schemas
from server.utils import errors, html_codes
from flask import Blueprint, make_response, jsonify
from flask_restful import Resource, Api
from server.core import tokens

schema = schemas.ServiceSchema()

class Service(Resource):
    
    decorators = [tokens.jwt_required] 

    def get(self, id):
        service = models.Service.query.get(id)
        if not service:
            return {},html_codes.HTTP_BAD_NOTFOUND

        response = json.loads(schema.dumps(service).data)
        
        return jsonify(service=response)

    def delete(self, id):
        return "deletes a Service with id :" + id

    def put(self, id):
        return "updates a Service with id :" + id

class ServiceList(Resource):
    
    decorators = [tokens.jwt_required]

    def get(self):
        services = models.Service.query.all()
        if not services:
            return {},html_codes.HTTP_BAD_NOTFOUND
        
        result = [json.loads(schema.dumps(s).data) for s in services]
 
        return jsonify(services=result)

    def post(self):
        return "creates a new Service"