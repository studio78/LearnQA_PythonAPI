import requests
_author__ = 'Stangli Adadurov'

response = requests.post("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
count_redirect = len(response.history)
print(f"Количество редиректов {count_redirect}, итоговый URL: {response.url} ")
