import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

_author__ = 'Stangli Adadurov'
# python -m pytest .\tests\test_user_auth.py --alluredir=test_results/


@allure.suite("Authorization cases")
class TestUserAuth(BaseCase):

    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.testcase("https://some.com/", "test_user_auth")
    @allure.title("Test Authentication")
    @allure.description("This test successfully authorize user by email and password")
    @allure.tag("Smoke", "Authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "Stangli Adadurov")
    @allure.link("https://some.com/", name="Website")
    @allure.testcase("ID-1001001")
    def test_user_auth(self):
        response2 = MyRequests.get("/user/auth", headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(response2, "user_id", self.user_id_from_auth_method,
                                             "User id from auth method is not equal to user id from check "
                                             "method")

    @allure.testcase("https://some2.com/", "test_negative_auth_check")
    @allure.title("Test negative authentication")
    @allure.description("This test checks authorization status w/o sending auth cookie or token")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        allure.dynamic.parameter("condition", condition)
        if condition == "no_cookie":
            response2 = MyRequests.get("/user/auth", headers={"x-csrf-token": self.token})
        else:
            response2 = MyRequests.get("/user/auth", cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(response2, "user_id", 0, f"User is authorized "
                                                                      f"with condition {condition}")
