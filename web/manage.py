# manage.py

import coverage

COV = coverage.coverage(
    branch=True,
    include='server/*',
    omit=[
        'tests/*',
        'server/config.py',
        'server/*/__init__.py'
    ]
)
COV.start()

import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from server.extensions import db
from server import app
from server.models import User
import server.factory as factory
import server.marshmallow_schemas as schemas

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""

    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='test@tourister.com',
                        password='TestTourister2017@',
                        admin=True))
    db.session.commit()


@manager.command
def create_fake_touristers():
    """Creates sample data."""
    
    test_user = factory.UserFactory()

    
    tourister = factory.TouristerFactory()
    tourister.ocupations = [factory.OccupationFactory() for i in range(3)] 
    tourister.languages = [factory.LanguageFactory() for i in range(2)] 
    
    trip = factory.TripFactory()
                               
    trip.highlights = [factory.TripHighlightFactory() for i in range(3)]

    trip.pricing =   factory.TripPricingFactory()
                
    trip.services = [ factory.ServiceFactory() for i in range(2) ]

    trip.services[0].perks = [ factory.ServicePerksFactory() for i in range(3)]

    trip.services[0].details = factory.RideshareDetailFactory()

    trip.services[0].details.additionalInfo = [factory.RideshareAdditionalInfoFactory() for i in range(4)]
    tourister.trips = [trip]

    tourister.payPalInfo = [factory.PaypalInfoFactory()]

    tourister.education = [factory.EducationFactory() for i in range(5)]

    tourister.socialNetworks =[ factory.SocialNetworkFactory() for i in range(4) ]

    testimonials = [factory.TestimonialFactory() for i in range(3)]
    
    for t in testimonials:
        t.user = test_user

    tourister.testimonials = testimonials 
    
    images = [factory.ImageFactory() for i in range(5)]
    activity = factory.ActivityFactory()
    activity.image = images[1]

    tourister.activities = [activity]
    tourister.images = images

    tourister_user = factory.UserFactory(email= factory.fake.email())
                    
    tourister_user.tourister = tourister


    db.session.add(tourister_user)
    db.session.commit()
    

if __name__ == '__main__':
    manager.run()
