# server/marshmallow_schemas.py

from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
import server.models  as models

class UserSchema(ModelSchema):
    class Meta:
        model = models.User

class BlacklistTokenSchema(ModelSchema):
    class Meta:
        model = models.BlacklistToken

class ServiceDetailSchema(ModelSchema):
    class Meta:
        model = models.ServiceDetail

class ServiceAdditionalInfoSchema(ModelSchema):
    class Meta:
        model = models.ServiceAdditionalInfo

class ServicePerksSchema(ModelSchema):
    class Meta:
        model = models.ServicePerks
        
class ServiceSchema(ModelSchema):
    perks = fields.Nested(ServicePerksSchema, many=True)
    additionalInfo = fields.Nested(ServiceAdditionalInfoSchema, many=True)
    details = fields.Nested(ServiceDetailSchema, many=True)
    class Meta:
        model = models.Service



class OccupationSchema(ModelSchema):
    class Meta:
        model = models.Occupation

class LanguageSchema(ModelSchema):
    class Meta:
        model = models.Language

class TripHighlightSchema(ModelSchema):
    class Meta:
        model = models.TripHighlight
  
class TripPricingSchema(ModelSchema):
    class Meta:
        model = models.TripPricing

class TripSchema(ModelSchema):
    highlighs = fields.Nested(TripHighlightSchema, many=True)
    pricing = fields.Nested(TripPricingSchema, many=True)
    services = fields.Nested(ServiceSchema, many=True)
    class Meta:
        model = models.Trip


class TouristerSchema(ModelSchema):
    
    class Meta:
        model = models.Tourister