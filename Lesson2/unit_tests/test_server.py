import sys
import os
import unittest

from lesson3.common.variables import RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME
from lesson3.server import process_client_massage


class TestServer(unittest.TestCase):
    bad_dict1 = {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }

    bad_dict2={
        RESPONSE: 400,
        ERROR: 'Unknown user'
    }
    good_dict = {
        RESPONSE: 200
    }

    def test_request(self):
        self.assertEqual(process_client_massage({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME:'Guest'}}), self.good_dict)

    def test_no_act(self):
        self.assertEqual(process_client_massage({TIME: 1.1, USER:{ACCOUNT_NAME:'Guest'}}),self.bad_dict1)

    def test_wrong_act(self):
        self.assertEqual(process_client_massage({ACTION: 'fgdg', TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.bad_dict1)
    def test_no_user(self):
        self.assertEqual(process_client_massage({ACTION: PRESENCE, TIME: 1.1}),
                         self.bad_dict1)
    def test_wrong_user(self):
        self.assertEqual(process_client_massage({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Ghost'}}),
                         self.bad_dict2)

if __name__ == '__main__':
    unittest.main()
