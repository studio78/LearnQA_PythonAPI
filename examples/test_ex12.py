import requests
from lib.base_case import BaseCase
_author__ = 'Stangli Adadurov'


class TestEx12(BaseCase):

    def test_ex12(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_header')
        print(response.headers)
        expected_header_name = "x-secret-homework-header"
        expected_header_value = "Some secret value"
        actual_header_value = self.get_header(response, expected_header_name)
        assert expected_header_value == actual_header_value, \
            (f"Ожидаемый header {expected_header_name} со значением {expected_header_value} "
             f"не соответствует полученному значению: {actual_header_value}")
