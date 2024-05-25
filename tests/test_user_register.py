from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest
import random
import string
import allure
_author__ = 'Stangli Adadurov'


@allure.epic("Register cases")
class TestUserRegister(BaseCase):

    @allure.description("Тест на успешное создание пользователя")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("Тест на невозможность создания пользователя с уже зарегестированным email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.description("Тест на невозможность создания пользователя с некорректным email")
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    params = [
        ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'email@m.ru'}, 'password'),
        ({'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'email@m.ru'}, 'username'),
        ({'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'email@m.ru'}, 'firstName'),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'email@m.ru'}, 'lastName'),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa'}, 'email'),
    ]

    @allure.description("Тест на невозможность создания пользователя с одним отсутствующим полем")
    @pytest.mark.parametrize('param', params)
    def test_create_user_wo_some_one_field(self, param):
        response = MyRequests.post("/user/", data=param[0])
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {param[1]}", \
            f"Unexpected response content {response.content}"

    params = ['username', 'firstName', 'lastName']

    @allure.description("Тест на невозможность создания пользователя с коротким именем в 1 знак")
    @pytest.mark.parametrize('field', params)
    def test_create_user_with_short_name(self, field):
        data = self.prepare_registration_data()
        data[field] = 'l'
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{field}' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.description("Тест на возможность создания пользователя с длинным именем в 250 знаков")
    @pytest.mark.parametrize('field', params)
    def test_create_user_with_long_name(self, field):
        data = self.prepare_registration_data()
        text = [random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(250)]
        data[field] = ''.join(text)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")
