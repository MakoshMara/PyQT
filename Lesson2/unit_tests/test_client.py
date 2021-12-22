import os
import sys
import unittest

from lesson3.client import create_presence, process_answer
from lesson3.common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR
# sys.path(os.path.join(os.getcwd(), '..'))


class TestClass(unittest.TestCase):
    def test_def_presense(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER:{ACCOUNT_NAME: 'Guest'}})

    def test_200(self):
        self.assertEqual(process_answer({RESPONSE: 200}), '200: все норм')

    def test_400(self):
        self.assertEqual(process_answer({RESPONSE: 400,ERROR:'Bad request'}), '400:Bad request')

    def test_no_response(self):
        self.assertRaises(ValueError, process_answer, {ERROR:'Bad request'})

if __name__ == '__main__':
    unittest.main()