import requests
import time
from json.decoder import JSONDecodeError
_author__ = 'Stangli Adadurov'

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# 1
response = requests.get(url)
try:
    parsed_response_text = response.json()
except JSONDecodeError:
    raise Exception("Response is not JSON format")
token = None
if "token" in parsed_response_text:
    token = parsed_response_text["token"]
else:
    raise Exception("Ключа token в JSON нет")
seconds = None
if "seconds" in parsed_response_text:
    seconds = parsed_response_text["seconds"]
else:
    raise Exception("Ключа seconds в JSON нет")
print(f"Token: {token}, seconds: {seconds}")

# 2
payload = {"token": token}
response = requests.get(url, params=payload)
try:
    parsed_response_text = response.json()
except JSONDecodeError:
    raise Exception("Response is not JSON format")
status = None
if "status" in parsed_response_text:
    status = parsed_response_text["status"]
else:
    raise Exception("Ключа status в JSON нет")
print(f"Status: {status}")
expected_status = "Job is NOT ready"
if status != expected_status:
    raise Exception(f'Полученный статус: "{status}" не соответствует ожидаемому: "{expected_status}"')

# 3
print(f"Please waiting {seconds} seconds")
time.sleep(seconds)

# 4
payload = {"token": token}
response = requests.get(url, params=payload)
try:
    parsed_response_text = response.json()
except JSONDecodeError:
    raise Exception("Response is not JSON format")
result = None
if "result" in parsed_response_text:
    result = parsed_response_text["result"]
else:
    raise Exception("Ключа result в JSON нет")
status = None
if "status" in parsed_response_text:
    status = parsed_response_text["status"]
else:
    raise Exception("Ключа status в JSON нет")
expected_status = "Job is ready"
if status != expected_status:
    raise Exception(f'Полученный статус: "{status}" не соответствует ожидаемому: "{expected_status}"')

print(f"Well done! Result: {result}, status: {status}")
