from requests import Response
import json

_author__ = 'Stangli Adadurov'

class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message=None):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        if error_message is None:
            error_message = (f"Для параметра {name} ожидаемое значение '{expected_value}' не соответствует полученному "
                             f"'{response_as_dict[name]}'")
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text '{response.text}'"
        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text '{response.text}'"
        assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}'. But it's present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code==expected_status_code, (f"Unexpected status code! Expected: {expected_status_code}."
                                                            f" Actual: {response.status_code}")
