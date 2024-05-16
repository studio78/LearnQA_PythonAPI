import requests
_author__ = 'Stangli Adadurov'

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1
payload = {"method": ""}
response = requests.get(url)
print(response.text)
print(response.status_code)

# 2
payload = {"method": "HEAD"}
response = requests.head(url, data=payload)
print(response.text)
print(response.status_code)

# 3
payload = {"method": "GET"}
response = requests.get(url, params=payload)
print(response.text)
print(response.status_code)


#4
reqs = ["GET", "POST", "PUT",  "DELETE"]
for req in reqs:
    payload = {"method": req}
    response1 = requests.get(url, params=payload)
    print(f"Запрос get c method={req} имеет response.text={response1.text} и response.status_code={response1.status_code}")
    response2 = requests.post(url, data=payload)
    print(f"Запрос post c method={req} имеет response.text={response2.text} и response.status_code={response2.status_code}")
    response3 = requests.put(url, data=payload)
    print(f"Запрос put c method={req} имеет response.text={response3.text} и response.status_code={response3.status_code}")
    response4 = requests.delete(url, data=payload)
    print(f"Запрос delete c method={req} имеет response.text={response4.text} и response.status_code={response4.status_code}")

