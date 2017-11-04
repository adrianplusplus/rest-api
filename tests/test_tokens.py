# tests/test_user_model.py

import unittest

from server import db, app
from server.models import User
from server.utils.tokens import encode_auth_token, decode_auth_token
from tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_no_jwt_max_age(self):
        app.config['JWT_MAX_AGE'] = None
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        ret_val = encode_auth_token(user.id)
        self.assertTrue(isinstance(ret_val, bytes))
        self.assertTrue(
            ret_val ==
            'unsupported type for timedelta seconds component: NoneType'
        )

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

        # second user
        self.assertTrue(decode_auth_token(
            auth_token.decode("utf-8")) == user.id)


if __name__ == '__main__':
    unittest.main()
