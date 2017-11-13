# server/marshmallow_schemas.py

from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
import server.models  as models


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
    details = fields.Nested(ServiceDetailSchema)
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
    highlights = fields.Nested(TripHighlightSchema, many=True)
    pricing = fields.Nested(TripPricingSchema)
    services = fields.Nested(ServiceSchema, many=True)
    class Meta:
        model = models.Trip

class PaypalInfoSchema(ModelSchema):
    class Meta:
        model = models.PaypalInfo

class EducationSchema(ModelSchema):
    class Meta:
        model = models.Education

class SocialNetworkSchema(ModelSchema):
    class Meta:
        model  = models.SocialNetwork

class ExperienceLevelSchema(ModelSchema):
    class Meta:
        model = models.ExperienceLevel

class TestimonialSchema(ModelSchema):
    class Meta:
        model = models.Testimonial

class ImageSchema(ModelSchema):
    class Meta:
        model = models.Image

class ActivitySchema(ModelSchema):
    image = fields.Nested(ImageSchema)
    class Meta:
        model = models.Activity


class TouristerSchema(ModelSchema):
    occupations = fields.Nested(OccupationSchema,many=True)
    languages = fields.Nested(LanguageSchema,many=True)
    allTrips = fields.Nested(TripSchema,many=True)
    payPalInfo = fields.Nested(PaypalInfoSchema)
    education = fields.Nested(EducationSchema, many=True)
    socialNetworks = fields.Nested(SocialNetworkSchema, many=True)
    experienceLevel = fields.Nested(ExperienceLevelSchema)
    testimonials = fields.Nested(TestimonialSchema, many=True)
    activities = fields.Nested(ActivitySchema, many=True)
    images = fields.Nested(ImageSchema, many=True)
    class Meta:
        model = models.Tourister

class UserSchema(ModelSchema):
    tourister = fields.Nested(TouristerSchema)
    class Meta:
        model = models.User