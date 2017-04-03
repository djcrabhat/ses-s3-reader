import unittest

import os
import unittest
import tempfile

from ses_s3_inbox import create_app

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        TEST_CONFIG = {
            "BUCKET": "test-bucket",
            "PREFIX": "email/"
        }
        self.app = create_app(config_dict=TEST_CONFIG)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_home(self):
        rv = self.client.get('/')
        self.assertIsNotNone(rv)
        self.assertEqual(rv.status_code, 200, "Homepage should return 200")

if __name__ == '__main__':
    unittest.main()