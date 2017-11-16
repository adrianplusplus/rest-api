# server/factory.py

from flask import Flask
from server.utils.logging_ext import setup_logger
from server.extensions import db, cache, bcrypt, cors
from server.models import User
import server.models as models
from server.faker_custom_providers import fake #instance of Faker()  to create fake data
import factory as factory_boy


def create_app(config='server.config.DevelopmentConfig', app=None):

    # Configure the app w.r.t Flask, databases, loggers.
    if app is None:
        app = Flask(__name__)
    app.config.from_object(config)
    return app


def setup_extensions(app):
    db.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    setup_logger(app)


def create_users(app):

    db.create_all()

    for user in app.config['DEFAULT_USERS']:

        found_user = User.query.filter_by(email=user['email']).first()

        if not found_user:
            new_user = User(
                email=user['email'],
                password=user['password'],
                admin=user['admin']
            )
            # insert the user
            db.session.add(new_user)

    db.session.commit()

class UserFactory(factory_boy.Factory):
    class Meta:
        model = models.User
        
    email = fake.email()
    password = fake.password()
    admin = False

class RideshareDetailFactory(factory_boy.Factory):
    class Meta:
        model = models.RideshareDetail
    
    price = fake.pyfloat(left_digits=3, right_digits=2,positive=True)
    miles = fake.pyfloat(left_digits=3, right_digits=2,positive=True)
    extraPricePerMile = fake.pyfloat(left_digits=2, right_digits=2,positive=True)
    make = fake.car_make()
    year = fake.year()
    model = fake.car_model(make=make)
    price = fake.pyfloat(left_digits=3, right_digits=2,positive=True)
    capacity = fake.random_digit_not_null()

class RideshareAdditionalInfoFactory(factory_boy.Factory):
    class Meta:
        model = models.RideshareAdditionalInfo
    value = fake.sentence()

class ServicePerksFactory(factory_boy.Factory):
    class Meta:
        model = models.ServicePerks
    value = fake.service_perks()

class ServiceFactory(factory_boy.Factory):
    class Meta:
        model = models.Service
    type = fake.service_type()  

class OccupationFactory(factory_boy.Factory):
    class Meta:
        model = models.Occupation
    
    name = fake.job()
    affiliation = fake.company()

class TripHighlightFactory(factory_boy.Factory):
    class Meta:
        model = models.TripHighlight

    value = fake.trip_highligh()

class TripPricingFactory(factory_boy.Factory):
    class Meta:
        model = models.TripPricing
    regular = fake.pyfloat(left_digits=3, right_digits=2,positive=True)
    regular = fake.random_digit_not_null()
    regular = fake.pyfloat(left_digits=2, right_digits=2,positive=True)

class TripFactory(factory_boy.Factory):
    class Meta:
        model = models.Trip
    
    name = fake.city() + " Trip"
    summary =  fake.sentence()
    city = fake.city()

class LanguageFactory(factory_boy.Factory):
    class Meta:
        model = models.Language
    name = fake.word(['English', 'Spanish', 'French', 'German'])
    proficiency = fake.word(['Excellent', 'Good', 'Average', 'Bad'])

class PaypalInfoFactory(factory_boy.Factory):
    class Meta:
        model = models.PaypalInfo
    email = fake.safe_email()

class EducationFactory(factory_boy.Factory):
    class Meta:
        model = models.Education
    
    school = fake.word(['SDSU', 'UCSD', 'USD', 'Rudgers', 'TTU', 'ANM'])
    degree = fake.word(['Liberal Arts', 'Computer Science', 'Sociology', 'Math', 'Statistics'])

class SocialNetworkFactory(factory_boy.Factory):
    class Meta:
        model = models.SocialNetwork
    
    type = fake.word(['Twitter', 'Facebook', 'Github', 'Google+', 'My Space'])
    src = fake.uri()

class TestimonialFactory(factory_boy.Factory):
    class Meta:
        model = models.Testimonial
    
    story = fake.paragraph()

class ImageFactory(factory_boy.Factory):
    class Meta:
        model = models.Image
    
    name = fake.file_name(extension='png')
    src = fake.image_url()
    type = fake.word(['Profile', 'Story', 'Main', 'Activity', 'Other'])

class ActivityFactory(factory_boy.Factory):
    class Meta:
        model = models.Activity
    
    detail = fake.paragraph()

class TouristerFactory(factory_boy.Factory):
    class Meta:
        model = models.Tourister


    firstname = fake.first_name()
    lastname = fake.last_name()
    username = fake.user_name()
    mainLocation = fake.city()
    story = fake.paragraph()


