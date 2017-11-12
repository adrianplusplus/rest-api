import json
import server.models as models
import server.marshmallow_schemas as schemas
from flask import Blueprint, make_response, jsonify
from flask_restful import Resource, Api
from server.utils.tokens import jwt_required

schema = schemas.ServiceSchema()

class Service(Resource):
    
    decorators = [jwt_required] 

    def get(self, id):
        service = models.Service.query.get(id)
        
        return json.loads(schema.dumps(service).data)

    def delete(self, id):
        return "deletes a Service with id :" + id

    def put(self, id):
        return "updates a Service with id :" + id

class ServiceList(Resource):
    
    decorators = [jwt_required]

    def get(self):
        services = models.Service.query.all()
        
        result = [json.loads(schema.dumps(s).data) for s in services]
        return result

    def post(self):
        return "creates a new Service"