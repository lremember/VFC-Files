import requests
import json
import httplib2
ud_data = {'csarId': 'f2f741d9-590e-40b9-9425-8f46f09e8bb6'}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
http = httplib2.Http()
resp, resp_content = http.request('http://159.138.61.203:30280/api/catalog/v1/nspackages',
    method="POST",
    body=json.dumps(ud_data),
    headers=headers)
print resp['status'], resp_content

