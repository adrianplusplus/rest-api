# server/models.py

from flask import current_app as app
from server.extensions import db, bcrypt
from sqlalchemy.orm import column_property


class Base(db.Model):
    """Base class for all the tables.
    Consists of two default columns `created_at` and `modified_at`.
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())


class User(Base):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    tourister = db.relationship('Tourister', backref='user',uselist=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.admin = admin


class BlacklistToken(Base):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    token = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, token):
        self.token = token


class RideshareDetail(Base):
    """ The detail of a service a tourister can offer """

    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    price = db.Column(db.Float)
    miles = db.Column(db.String(20))
    extraPricePerMile = db.Column(db.Float)
    make = db.Column(db.String(40))
    year = db.Column(db.Integer)
    model = db.Column(db.String(20))
    capacity = db.Column(db.Integer)

    additionalInfo = db.relationship(
        'RideshareAdditionalInfo', backref='rideshare', lazy='dynamic')


class RideshareAdditionalInfo(Base):
    """ Additional info that can be added to a tourister service """
 
    rideshare_detail_id = db.Column(db.Integer, db.ForeignKey('rideshare_detail.id'), nullable=False)

    value = db.Column(db.String(100))
    


class ServicePerks(Base):
    """ perks that can be added to a tourister service """
 
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    value = db.Column(db.String(100))
    


class Service(Base):
    """ services a tourister can offer """

    __tablename__ = 'services'

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    
    type = db.Column(db.String(30))
    perks = db.relationship('ServicePerks', backref='service', lazy='dynamic')
    details = db.relationship(
        'RideshareDetail', backref='service', uselist=False)


class Occupation(Base):
    """ Occupations touristers can exercise (to find matches) """

    __tablename__ = 'occupations'

    tourister_id = db.Column(db.Integer, db.ForeignKey('touristers.id'), nullable=False)

    name = db.Column(db.String(30), nullable=False)
    affiliation = db.Column(db.String(30))


class TripHighlight(Base):
    """ highlights a trip can have """

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)

    value = db.Column(db.String(50), nullable=False)


class TripPricing(Base):
    """ different pricing models for trips a tourister can provide """

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    
    regular = db.Column(db.Float)
    tripDuration = db.Column(db.Float)
    overtimePrice = db.Column(db.Float)


class Trip(Base):
    """ trips a tourister has done """

    __tablename__ = 'trips'

    tourister_id = db.Column(db.Integer, db.ForeignKey('touristers.id'), nullable=False)

    name = db.Column(db.String(30))
    summary = db.Column(db.String(500))
    city = db.Column(db.String(30))

    highlights = db.relationship('TripHighlight', backref='service', lazy='dynamic')
    pricing = db.relationship('TripPricing', backref='service', uselist=False)
    services = db.relationship('Service', backref='service', lazy='dynamic')


class Language(Base):
    """ languages a tourister can speak/understand """

    __tablename__ = 'languages'

    tourister_id = db.Column(db.Integer, db.ForeignKey('touristers.id'), nullable=False)

    name = db.Column(db.String(10), nullable=False)
    proficiency = db.Column(db.String(10), nullable=False)

class PaypalInfo(Base):
    """ information needed to use user's paypal """

    tourister_id = db.Column(db.Integer, db.ForeignKey('touristers.id'), nullable=False)

    email = db.Column(db.String(100), nullable=False)

class Education(Base):
    """ education of a tourister """

    tourister_id = db.Column(db.Integer, db.ForeignKey('touristers.id'), nullable=False)

    school = db.Column(db.String(30))
    degree = db.Column(db.String(30))

class SocialNetwork(Base):
    """ different social networks of a tourister """

    tourister_id = db.Column(db.Integer, db.ForeignKey('touristers.id'), nullable=False)

    type = db.Column(db.String(30))
    src = db.Column(db.String(200))


class Testimonial(Base):
    """ testimonials given by touristees """

    tourister_id = db.Column(db.Integer, db.ForeignKey('touristers.id'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", uselist=False)
    story = db.Column(db.String(800), nullable=False)

class Image(Base):
    """ for storing image urls """

    name = db.Column(db.String(50))
    src = db.Column(db.String(1000))
    type = db.Column(db.String(50))

class Activity(Base):
    """ activities a tourister has done """
    
    tourister_id = db.Column(db.Integer, db.ForeignKey('touristers.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    
    detail = db.Column(db.String(300), nullable=False)

    image = db.relationship("Image", uselist=False)

class TouristerImage(db.Model):
    """ used to associate many to many images to touristers """
    __tablename__ = 'tourister_images'
    __table_args__ = (db.PrimaryKeyConstraint('tourister_id','image_id'), )

    tourister_id = db.Column(db.Integer, db.ForeignKey('touristers.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable = False)

class Tourister(Base):
    """ defines what a tourister can be """

    __tablename__ = 'touristers'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    middlename = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False)
    mainLocation = db.Column(db.String(30))
    story = db.Column(db.String(800))
    
    occupations = db.relationship('Occupation', backref='tourister', lazy='dynamic')
    languages = db.relationship('Language', backref='tourister', lazy='dynamic')
    trips = db.relationship('Trip', backref='tourister', lazy='dynamic')
    paypalInfo = db.relationship('PaypalInfo', backref='tourister')
    education = db.relationship('Education', backref='tourister', lazy='dynamic')
    socialNetworks = db.relationship("SocialNetwork", backref='tourister', lazy='dynamic')
    testimonials = db.relationship("Testimonial", backref='tourister', lazy='dynamic')
    activities = db.relationship('Activity', backref='tourister', lazy='dynamic')
    images = db.relationship("Image", secondary='tourister_images')
