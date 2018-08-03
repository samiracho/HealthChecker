import os
import requests
from error import HealthError
import re


class Check(object):

    def __init__(self, endpoints):
        """
        :param endpoints: Dictionary with the rules to check the endpoints
        """
        self.endpoints = endpoints["checks"]
        self.notify = endpoints["notificationEndpoint"]
        self.errors_list = []

    def check_endpoints(self):
        for endpoint in self.endpoints:
            self.do_request(endpoint)

    def send_notifications(self):
        for my_error in self.errors_list:
            Check.send_notification(my_error, self.notify)

    def do_request(self, endpoint: dict):
        """
        Does a health check applying the service config rules
        :param endpoint: Dictionary with the endpoint and the rules to check
        """
        request = endpoint["request"]
        errors = []
        verify_ssl = request.get('verifySSL', True)
        try:
            response = requests.request(method=request["method"], headers=request.get('headers', ""), url=request["endpoint"], data=request.get('body', ""), verify=verify_ssl, timeout=(request.get('connectTimeout', 5), request.get('readTimeout', 5)))
            Check.check_status_codes(response, endpoint, errors)
            Check.check_body_text(response, endpoint, errors)

        # We want to notify only the exceptions related to the endpoint failures.
        except (requests.HTTPError, requests.Timeout, requests.TooManyRedirects, requests.ConnectionError) as health_exceptions:
            errors.append(str(health_exceptions))
        except (requests.URLRequired, Exception) as e:
            print("ERROR: Internal error. " + str(e))
        finally:
            if errors:
                self.errors_list.append(HealthError(endpoint["service"], errors))

    @staticmethod
    def check_status_codes(http_response: object, endpoint: dict, errors: list):
        """
        Checks
        :param http_response: request http response
        :param endpoint: endpoint rules
        :param errors: Errors list
        """
        response_conditions = endpoint["response"]
        if "codes" in response_conditions:
            if http_response.status_code not in response_conditions["codes"] and len(response_conditions["codes"]) > 0:
                errors.append("Status code check failed. \n Expected status codes: "+str(response_conditions["codes"])+"\nResponse status code:" + str(http_response.status_code))

    @staticmethod
    def check_body_text(http_response: object, endpoint: dict, errors: list):
        """
        Checks if a text is in the response body
        :param http_response: request http response
        :param endpoint: endpoint rules
        :param errors: Errors list
        """

        response_conditions = endpoint["response"]
        http_response_text = http_response.text if http_response.text else ""
        if "body" in response_conditions:
            if not re.search(response_conditions["body"], http_response_text, flags=re.M):
                errors.append("Body content check failed. \n Text not found: " + response_conditions["body"])

    @staticmethod
    def send_notification(data: HealthError, notify: dict):
        """
        Sends a health check notification
        :param data: HealthError object with the errors found checking an endpoint
        :param notify: Dictionary with notification endpoint values
        """

        if os.environ.get('HK_NOTIFY_TOKEN') is None:
            raise Exception("ERROR: Auth token missing. Make sure the env variable HK_NOTIFY_TOKEN is set")
        else:
            notification_token = os.environ['HK_NOTIFY_TOKEN']
            notify["headers"]["Authorization"] = notify["headers"]["Authorization"].format(notification_token)

        response = requests.request(method=notify["method"], headers=notify["headers"], url=notify["url"], json=data.getJson())

        if response.ok:
            print("OK: Health check notification sent:" + str(data.getJson()))
        else:
            print("ERROR: Health check notification failed: " + response.content)
