from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
import pytest
from requests import Response
_author__ = 'Stangli Adadurov'


@allure.epic("User Edit cases")
class TestUserEdit(BaseCase):

    @allure.step("Проверка некорректного ответа и сообщения об ошибке")
    def negative_assert(self, response: Response, error_text):
        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_has_key(response, "error")
        Assertions.assert_json_value_by_name(response, "error",
                                             error_text, f"Не корректный текст ошибки: "
                                                         f"{self.get_json_value(response, 'error')}")

    @allure.description("Тест на редактирование только что созданного пользователя")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")
        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}, data={"firstName": new_name})
        Assertions.assert_code_status(response3, 200)
        # GET
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "firstName", new_name,
                                             "Wrong name of the user after edit")

    @allure.description("Тест на невозможность изменить данные пользователя, будучи неавторизованными")
    def test_edit_user_wo_auth(self):
        response = MyRequests.put(f"/user/2", data={"firstName": "Changed Name"})
        self.negative_assert(response, "Auth token not supplied")

    @allure.description("Тест на невозможность изменить данные пользователя, будучи авторизованными другим "
                        "пользователем")
    def test_edit_user_with_auth_other_user(self):
        # REGISTER USER 1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)
        email = register_data1['email']
        password = register_data1['password']
        # REGISTER USER 2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)
        user_id = self.get_json_value(response2, "id")
        # LOGIN BY USER 1
        data = {
            'email': email,
            'password': password
        }
        response3 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")
        # EDIT USER 2
        response4 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                   data={"firstName": "Changed Name"})
        self.negative_assert(response4, "This user can only edit their own data.")

    params = [
        ({'email': 'emailtest.ru'}, 'Invalid email format'),
        ({'firstName': 'l'}, 'The value for field `firstName` is too short'),
    ]

    @allure.description("Тест на невозможность изменить данные на некорректные данные в полях")
    @pytest.mark.parametrize('param', params)
    def test_edit_user_with_incorrect_same_field(self, param):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")
        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        # EDIT
        response3 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}, data=param[0])
        self.negative_assert(response3, param[1])

