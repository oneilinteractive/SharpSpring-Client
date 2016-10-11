from random import randint

import unittest

from sharpspringclient import SharpSpringRequest, SharpSpringFormRequest


class RequestTests(unittest.TestCase):

    def setUp(self):
        self.account_id = 'id_{}'.format(randint(1000, 1000000))
        self.api_secret_key = 'key_{}'.format(randint(1000, 1000000))
        self.request = SharpSpringRequest(api_account_id=self.account_id,
            api_secret_key=self.api_secret_key)

    def test_can_do_this(self):
        self.assertTrue(False)


class RequestFormTests(unittest.TestCase):

    def test_can_do_this(self):
        self.assertTrue(False)
