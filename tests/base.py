# tests/base.py


from flask_testing import TestCase

from server import app
from server.extensions import db
from server.factory import create_app, create_users


class BaseTestCase(TestCase):

    def create_app(self):
        new_app = create_app('server.config.TestingConfig', app)
        create_users(new_app)
        return new_app

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
