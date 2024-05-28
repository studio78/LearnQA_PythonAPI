from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
_author__ = 'Stangli Adadurov'


@allure.epic("User delete cases")
class TestUserDelete(BaseCase):

    @allure.description("Тест невозможности удаления пользователя с ID 2")
    def test_try_delete_user_vinkotov(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        response2 = MyRequests.delete(f"/user/2", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.negative_assert(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.description("Тест на удаление только что созданного пользователя")
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
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
        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}", headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 200)
        # GET
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == f"User not found", \
            f"Unexpected response content {response4.content}"

    @allure.description("Тест на невозможность удалить пользователя, будучи авторизованными другим пользователем")
    def test_delete_user_with_auth_other_user(self):
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
        # DELETE USER 2
        response4 = MyRequests.delete(f"/user/{user_id}", headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.negative_assert(response4, "This user can only delete their own account.")
