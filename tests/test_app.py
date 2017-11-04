# tests/test_api.py

import unittest
import logging
from tests.base import BaseTestCase

logger = logging.getLogger(__name__)


class TestApp(BaseTestCase):

    def test_app_root(self):
        """ Test for pulling data from the data-filter  """
        with self.client:
            response = self.client.get(
                '/'
            )
            data = response.get_data().decode()
            self.assertTrue(data == 'App is running!')
            self.assertEqual(response.status_code, 200)

            # execute logger
            logger.info('Testing app logger')


if __name__ == '__main__':
    unittest.main()
