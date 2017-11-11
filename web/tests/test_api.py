# tests/test_api.py

import unittest
import json
from tests.base import BaseTestCase
from tests.helpers import login_user, register_user
from server.utils import html_codes


class TestAPI(BaseTestCase):

    def test_get_data(self):
        """ Test for guarded api """
        with self.client:
            # user login
            resp_login = login_user(
                self,
                'test@qti.qualcomm.com',
                'TestAvante2017@'
            )
            data = json.loads(resp_login.get_data().decode())
            # valid api call
            resp_get_data = self.client.get(
                '/api/get_data',
                headers={
                    'Authentication-Token': 'Bearer ' + data['auth_token']
                }
            )
            data_api = json.loads(resp_get_data.get_data().decode())
            self.assertTrue(
                data_api['Heroes']
            )
            self.assertEqual(resp_get_data.status_code,
                             html_codes.HTTP_OK_BASIC)

    def test_protected_get_data(self):
        """ Test for protected api against user with permissions """
        with self.client:
            # user login
            resp_login = login_user(
                self,
                'test@qti.qualcomm.com',
                'TestAvante2017@'
            )

            # valid api call
            resp_get_data = self.client.get(
                '/api/protected_get_data',
                headers={
                    'Authentication-Token': 'Bearer ' + json.loads(
                        resp_login.get_data().decode()
                    )['auth_token']
                }
            )
            data_api = json.loads(resp_get_data.get_data().decode())
            self.assertTrue(
                data_api['Heroes']
            )

    def test_no_permissions_protected_get_data(self):
        """ Test protected api against user without permissions """
        with self.client:
            # user registration
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            # api call
            resp_get_data = self.client.get(
                '/api/protected_get_data',
                headers={
                    'Authentication-Token': 'Bearer ' + json.loads(
                        resp_register.get_data().decode()
                    )['auth_token']
                }
            )
            self.assertEqual(resp_get_data.status_code,
                             html_codes.HTTP_BAD_FORBIDDEN)

    def test_app_root(self):
        """ Test for non json returning guarded api """
        with self.client:

            # user login
            resp_login = login_user(
                self,
                'test@qti.qualcomm.com',
                'TestAvante2017@'
            )
            data = json.loads(resp_login.get_data().decode())
            # valid api call
            resp_get_data = self.client.get(
                '/api/get_data_non_json',
                headers={
                    'Authentication-Token': 'Bearer ' + data['auth_token']
                }
            )
            data_api = resp_get_data.get_data().decode()
            self.assertTrue(
                data_api == 'Non JSON data!'
            )
            self.assertEqual(resp_get_data.status_code,
                             html_codes.HTTP_OK_BASIC)


if __name__ == '__main__':
    unittest.main()
