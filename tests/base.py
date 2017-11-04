# tests/base.py


from flask_testing import TestCase

from server import app, db
from server.models import User
from server.factory import create_app, create_user


class BaseTestCase(TestCase):

    def create_app(self):
        new_app = create_app('server.config.TestingConfig', app)
        create_user(new_app, db, User)
        return new_app

    def setUp(self):
        db.create_all()
        user = User(email="ad@min.com", password="admin_user")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
