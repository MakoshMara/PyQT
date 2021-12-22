
import unittest
import json

from lesson3.common.utils import send_meccage, get_message
from lesson3.common.variables import ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestSoket:

    def __init__(self,test_dict):
        self.test_dict = test_dict
        self.encoded_ms = None
        self.received_ms = None

    def send(self, message_to_send):
        json_test_massage = json.dumps(self.test_dict)
        self.encoded_ms = json_test_massage.encode(ENCODING)
        self.received_ms = message_to_send

    def recv(self,max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)

class TestUtils(unittest.TestCase):
    test_dict_send = {
        ACTION:PRESENCE,
        TIME:11111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }

    test_dict_re_good = {RESPONSE:200}
    test_dict_re_bad = {
        RESPONSE: 400,
        ERROR:'Bad request'
    }

    def test_send_ok_message(self):
        test_soket = TestSoket(self.test_dict_send)
        send_meccage(test_soket,self.test_dict_send)
        self.assertEqual(test_soket.encoded_ms, test_soket.received_ms)

    def test_send_bad_message(self):
        self.assertRaises(TypeError,send_meccage, TestSoket, "wfsdfsdf")

    def test_get_good_message(self):
        test_sock_ok = TestSoket(self.test_dict_re_good)
        self.assertEqual(get_message(test_sock_ok),self.test_dict_re_good)


    def test_get_bad_message(self):
        test_sock_err = TestSoket(self.test_dict_re_bad)
        self.assertEqual(get_message(test_sock_err), self.test_dict_re_bad)

if __name__ == '__main__':
    unittest.main()
