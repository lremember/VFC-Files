import requests
import json
import httplib2
ud_data = {'csarId': '20c28260-5078-4729-847f-f8b0a3bff8d9'}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
http = httplib2.Http()
resp, resp_content = http.request('http://159.138.61.203:30280/api/catalog/v1/vnfpackages',
    method="POST",
    body=json.dumps(ud_data),
    headers=headers)
print resp['status'], resp_content

