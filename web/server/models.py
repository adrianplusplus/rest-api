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
    tourister = db.relationship('Tourister', backref='user', lazy='dynamic')

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.admin = admin


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()


class ServiceDetail(db.Model):
    """ The detail of a service a tourister can offer """

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    miles = db.Column(db.String(20))
    extraPricePerMile = db.Column(db.Float)
    make = db.Column(db.String(40))
    year = db.Column(db.Integer)
    model = db.Column(db.String(20))
    capacity = db.Column(db.Integer)
    service_id = db.Column(db.Integer, db.ForeignKey(
        'services.id'), nullable=False)


class ServiceAdditionalInfo(db.Model):
    """ Additional info that can be added to a tourister service """

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100))
    service_id = db.Column(db.Integer, db.ForeignKey(
        'services.id'), nullable=False)


class ServicePerks(db.Model):
    """ perks that can be added to a tourister service """

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100))
    service_id = db.Column(db.Integer, db.ForeignKey(
        'services.id'), nullable=False)


class Service(db.Model):
    """ services a tourister can offer """

    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    perks = db.relationship('ServicePerks', backref='service', lazy='dynamic')
    additionalInfo = db.relationship(
        'ServiceAdditionalInfo', backref='service', lazy='dynamic')
    details = db.relationship(
        'ServiceDetail', backref='service', lazy='dynamic')


class Occupation(db.Model):
    """ ?? """

    __tablename__ = 'occupations'

    id = db.Column(db.Integer, primary_key=True)
    tourister_id = db.Column(db.Integer, db.ForeignKey(
        'touristers.id'), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    affiliation = db.Column(db.String(30))


class TripHighlight(db.Model):
    """ highlights a trip can have """

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    value = db.Column(db.String(50), nullable=False)


class TripPricing(db.Model):
    """ different pricing models for trips a tourister can provide """

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    regular = db.Column(db.Float)
    tripDuration = db.Column(db.Float)
    overtimePrice = db.Column(db.Float)


class Trip(db.Model):
    """ trips a tourister has done """

    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    tourister_id = db.Column(db.Integer, db.ForeignKey(
        'touristers.id'), nullable=False)
    name = db.Column(db.String(30))
    tripSummary = db.Column(db.String(500))
    city = db.Column(db.String(30))
    highlights = db.relationship(
        'TripHighlight', backref='service', lazy='dynamic')
    pricing = db.relationship('TripPricing', backref='service', lazy='dynamic')
    services = db.relationship('Service', backref='service', lazy='dynamic')


class Language(db.Model):
    """ languages a tourister can speak/understand """

    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    tourister_id = db.Column(db.Integer, db.ForeignKey(
        'touristers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    proficiency = db.Column(db.String(10), nullable=False)


class Tourister(db.Model):
    """ defines what a tourister can be """

    __tablename__ = 'touristers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    ocupations = db.relationship(
        'Occupation', backref='tourister', lazy='dynamic')
    languages = db.relationship(
        'Language', backref='tourister', lazy='dynamic')
    allTrips = db.relationship('Trip', backref='tourister', lazy='dynamic')
