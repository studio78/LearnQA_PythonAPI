import requests
from lib.base_case import BaseCase
_author__ = 'Stangli Adadurov'


class TestEx11(BaseCase):

    def test_ex11(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
        print(response.cookies)
        expected_cookie_name = "HomeWork"
        expected_cookie_value = "hw_value"
        actual_cookie_value = self.get_cookie(response, expected_cookie_name)
        assert expected_cookie_value == actual_cookie_value, \
            (f"Ожидаемое cookie {expected_cookie_name} со значением {expected_cookie_value} "
             f"не соответствует полученному значениею: {actual_cookie_value}")
