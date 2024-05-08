import json
_author__ = 'Stangli Adadurov'

json_text = ('{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And '
             'this is a second message","timestamp":"2021-06-04 16:41:01"}]}')

obj = json.loads(json_text)
array = "messages"
key = "message"
if array in obj:
    if key in obj[array][1]:
        print(obj[array][1][key])
    else:
        print(f"Ключа {key} в JSON нет")
else:
    print(f"Массива {array} в JSON нет")
