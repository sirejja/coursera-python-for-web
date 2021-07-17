import requests
import json
headers = {'Authorization': 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'}
response = requests.post('https://datasend.webpython.graders.eldf.ru/submissions/1/', headers=headers)
print(json.loads(response.content.decode('utf-8')))

import base64
print(base64.b64encode(b'alibaba:40razboinikov'))

headers = {'Authorization': 'Basic YWxpYmFiYTo0MHJhemJvaW5pa292'}
response = requests.put('https://datasend.webpython.graders.eldf.ru/submissions/secretlocation/', headers=headers)
print(json.loads(response.content.decode('utf-8')))