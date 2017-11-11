# tests/test_auth.py


import time
import json
import unittest

from server.extensions import db
from server.models import User, BlacklistToken
from server.utils import html_codes
from tests.base import BaseTestCase
from tests.helpers import login_user, register_user


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.get_data().decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['token_max_age'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, html_codes.HTTP_OK_CREATED)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = User(
            email='joe@gmail.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.get_data().decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code,
                             html_codes.HTTP_BAD_FORBIDDEN)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            register_user(self, 'joe@gmail.com', '123456')
            # registered user login
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.get_data().decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['token_max_age'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code,
                             html_codes.HTTP_OK_BASIC)

    def test_registration_invalid(self):
        """ Test for registration with invalid data """
        with self.client:
            # user registration
            resp = self.client.post(
                '/auth/register',
                data=json.dumps(''),
                content_type='application/json',
            )

            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Some error occurred. Please try again.'
            )
            self.assertTrue(resp.content_type == 'application/json')
            self.assertEqual(resp.status_code,
                             html_codes.HTTP_SERVER_ERROR)

    def test_user_login_invalid(self):
        """ Test for login with invalid data """
        with self.client:
            # registered user login
            response = self.client.post(
                '/auth/login',
                data=json.dumps(''),
                content_type='application/json',
            )
            data = json.loads(response.get_data().decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Some error occurred. Please try again.'
            )
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code,
                             html_codes.HTTP_SERVER_ERROR)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.get_data().decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code,
                             html_codes.HTTP_BAD_NOTFOUND)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user login
            resp_login = login_user(
                self,
                'test@qti.qualcomm.com',
                'TestAvante2017@'
            )
            data_login = json.loads(resp_login.get_data().decode())
            # valid token logout
            resp_logout = self.client.post(
                '/auth/logout',
                headers={
                    'Authentication-Token': 'Bearer ' +
                    data_login['auth_token']
                }
            )
            data_logout = json.loads(resp_logout.get_data().decode())
            self.assertTrue(data_logout['status'] == 'success')
            self.assertTrue(
                data_logout['message'] == 'Successfully logged out.'
            )
            self.assertEqual(resp_logout.status_code,
                             html_codes.HTTP_OK_BASIC)
            # try to access guarded endpoint again
            response = self.client.post(
                '/auth/logout',
                headers={
                    'Authentication-Token': 'Bearer ' +
                    data_login['auth_token']
                }
            )
            data = json.loads(response.get_data().decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Token blacklisted. Please log in again.'
            )
            self.assertEqual(response.status_code,
                             html_codes.HTTP_BAD_UNAUTHORIZED)

    def test_invalid_logout(self):
        """ Testing logout after the token expires """
        with self.client:
            # user registration
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            data_login = json.loads(resp_register.get_data().decode())
            # invalid token logout
            time.sleep(3)
            response = self.client.post(
                '/auth/logout',
                headers={
                    'Authentication-Token': 'Bearer ' +
                    data_login['auth_token']
                }
            )
            data = json.loads(response.get_data().decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code,
                             html_codes.HTTP_BAD_UNAUTHORIZED)

    def test_no_jwt_in_header(self):
        """ Test for a request without jwt """
        with self.client:
            register_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                '/auth/logout'
            )
            data = json.loads(response.get_data().decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code,
                             html_codes.HTTP_BAD_FORBIDDEN)

    def test_invalid_token_error(self):
        """ Test for a request with an invalid token """
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_register.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.post(
                '/auth/logout',
                headers={
                    'Authentication-Token': 'Bearer 1245'
                }
            )
            data = json.loads(response.get_data().decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.'
            )
            self.assertEqual(response.status_code,
                             html_codes.HTTP_BAD_UNAUTHORIZED)


if __name__ == '__main__':
    unittest.main()
