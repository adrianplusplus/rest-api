# tests/test_app.py

import unittest
from tests.base import BaseTestCase
from server.utils import html_codes


class TestApp(BaseTestCase):

    def test_app_root(self):
        """ Test for checking app """
        with self.client:
            response = self.client.get(
                '/'
            )
            data = response.get_data().decode()
            self.assertTrue(data == 'App is running!')
            self.assertEqual(response.status_code,
                             html_codes.HTTP_OK_BASIC)


if __name__ == '__main__':
    unittest.main()
