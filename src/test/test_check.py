import sys
import os
import unittest
from mock import Mock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from check import Check


class TestConfigMethods(unittest.TestCase):

    def test_check_status_codes_not_found(self):

        '''An error should be added to the errors list if the status code is not found in the codes list'''
        http_response = Mock(status_code=200)
        errors = []
        endpoint = {'response': {'codes': [100, 101, 102]}}

        Check.check_status_codes(http_response, endpoint, errors)

        result = len(errors)
        self.assertEqual(result, 1)

    def test_check_status_codes_found(self):
        '''No errors should be added to the errors list if the status code is not found in the codes list'''
        http_response = Mock(status_code=200)
        errors = []
        endpoint = {'response': {'codes': [100, 101, 200]}}

        Check.check_status_codes(http_response, endpoint, errors)

        result = len(errors)
        self.assertEqual(result, 0)

    def test_check_no_http_status_code(self):
        '''If there is no status code it should raise an exception'''
        http_response = Mock(status=None)
        errors = []
        endpoint = {'response': {'codes': [100, 101, 200]}}

        Check.check_status_codes(http_response, endpoint, errors)
        self.assertRaises(Exception)

    def test_check_status_codes_list_empty(self):
        '''No errors should be added to the errors list if the codes list is empty'''
        http_response = Mock(status_code=200)
        errors = []
        endpoint = {'response': {'codes': []}}

        Check.check_status_codes(http_response, endpoint, errors)

        result = len(errors)
        self.assertEqual(result, 0)

    def test_check_status_no_codes_list(self):
        '''No errors should be added to the errors list if code list doesnt exist'''
        http_response = Mock(status_code=200)
        errors = []
        endpoint = {'response': {}}

        Check.check_status_codes(http_response, endpoint, errors)

        result = len(errors)
        self.assertEqual(result, 0)

    def test_check_body_text_found(self):
        '''No errors should be added to the errors list if the body is found in the response text'''
        http_response = Mock(text="my text \n foo\nbarFooo")
        errors = []
        endpoint = {'response': {'body': "foo\nb"}}

        Check.check_status_codes(http_response, endpoint, errors)

        result = len(errors)
        self.assertEqual(result, 0)

    def test_check_body_text_not_found(self):
        '''An error should be added to the errors list if the body is found in the response text'''
        http_response = Mock(text="my text \n foo\nbarFooo")
        errors = []
        endpoint = {'response': {'body': "NOTFOUND"}}

        Check.check_status_codes(http_response, endpoint, errors)

        result = len(errors)
        self.assertEqual(result, 0)

    def test_check_body_no_body(self):
        '''No error should be added to the errors list if the body attribute doesnt exist'''
        http_response = Mock(text="my text \n foo\nbarFooo")
        errors = []
        endpoint = {'response': {}}

        Check.check_status_codes(http_response, endpoint, errors)

        result = len(errors)
        self.assertEqual(result, 0)

    def test_check_endpoints_timeout(self):

        endpoint = {'notificationEndpoint': {'url': ''}, 'checks': [{'request': {'endpoint': 'http://127.0.0.1:1',  'method': 'GET', 'connectTimeout': 0.001}, 'response': {'codes': [200]}, 'service': 'Gitlab'}]}

        my_check = Check(endpoint)
        my_check.check_endpoints()

        result = len(my_check.errors_list)
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
