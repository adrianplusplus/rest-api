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
import server.models as models

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
def create_data():
    """Creates sample data."""
    

    tourister = models.Tourister(firstname="Adrian",
                                 lastname="Galicia",
                                 middlename="Omar",
                                 username="adrianplusplus",
                                 story="from tijuas to aqui")
    tourister.ocupations = [
                    models.Occupation(name="Student", affiliation="SDSU"),
                    models.Occupation(name="Engineer", affiliation="Citigroup")
                  ]
    tourister.languages = [
                    models.Language(name="Spanish", proficiency="Excellent"),
                    models.Language(name="English", proficiency="Good")
                ]
    trip = models.Trip(tourister_id = 1,
                               name='Baja Road Trip',
                               summary='This is a cool trip',
                               city='Tijuana, MX')
                               
    trip.highlights = [models.TripHighlight(trip_id = 1,
                                     value='I can kiss you as much you want.')]

    trip.pricing =   models.TripPricing(trip_id=1,
                                regular=150,
                                tripDuration=10,
                                overtimePrice=10)
                
    trip.services = [
                 models.Service(trip_id=1, type='Car Share'),
                 models.Service(trip_id=1, type='Housing')
               ]

    trip.services[0].perks = [
                        models.ServicePerks(value='first 60 mi free'),
                        models.ServicePerks(value='50% discount after 120 mi')
                    ]

    trip.services[0].details = models.ServiceDetail(price=50,
                                          miles=50,
                                          extraPricePerMile=10,
                                          make='Volkw Wagen',
                                          year='2013',
                                          model='jetta',
                                          capacity=4
                                            )
    trip.services[0].details.additionalInfo = [
                        models.ServiceAdditionalInfo(service_detail_id=1, value='Quema cocos')
                        ]
    tourister.allTrips = [trip]

    tourister.payPalInfo = models.PaypalInfo(email="my_paypal_info@gmail.com")

    tourister.education = [models.Education(school='SDSU', degree="Computer Science")]

    tourister.socialNetworks = [
        models.SocialNetwork(type="FaceBook", src="facebook.com/adrianplusplus"),
        models.SocialNetwork(type="Twiter", src="twiter.com/adrianplusplus")
        ]

    tourister.experienceLevel = models.ExperienceLevel(customersServed=50, rating=4.5)

    tourister.testimonials = [models.Testimonial(username="anotherUserName", story="had a great time")]
    
    images = [
        models.Image(name='photo1',src='https://www.google.com.ar/imgres?imgurl=http%3A%2F%2Fwww.gettyimages.com%2Fgi-resources%2Fimages%2FEmbed%2Fnew%2Fembed2.jpg&imgrefurl=http%3A%2F%2Fwww.gettyimages.com%2Fresources%2Fembed&docid=A2VKv0m3cptz9M&tbnid=m64vr72lvlG29M%3A&vet=10ahUKEwjHjoSnp7vXAhXFfZAKHdEfAtQQMwjmASgHMAc..i&w=500&h=359&bih=987&biw=1920&q=images&ved=0ahUKEwjHjoSnp7vXAhXFfZAKHdEfAtQQMwjmASgHMAc&iact=mrc&uact=8',type='profile'),
        models.Image(name='photo2',src='https://www.google.com.ar/imgres?imgurl=https%3A%2F%2Fcdn.pixabay.com%2Fphoto%2F2016%2F10%2F27%2F22%2F53%2Fheart-1776746_960_720.jpg&imgrefurl=https%3A%2F%2Fpixabay.com%2Fen%2Fheart-sweetheart-leaf-autumn-maple-1776746%2F&docid=9HgwBjd9hqB0oM&tbnid=KRZIiHKQUAZCCM%3A&vet=10ahUKEwjHjoSnp7vXAhXFfZAKHdEfAtQQMwjpASgKMAo..i&w=960&h=668&bih=987&biw=1920&q=images&ved=0ahUKEwjHjoSnp7vXAhXFfZAKHdEfAtQQMwjpASgKMAo&iact=mrc&uact=8',type='other')
    ]
    activity = models.Activity(detail = "some dtetails about the activity")
    activity.image = images[1]

    tourister.activities = [activity]
    tourister.images = images

    tourister_user = User(email='tourister1@tourister.com',
                        password='TestTourister2017@',
                        admin=False)
                    
    tourister_user.tourister = tourister


    db.session.add(tourister_user)
    db.session.commit()
    

if __name__ == '__main__':
    manager.run()
