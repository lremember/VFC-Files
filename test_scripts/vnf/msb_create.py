import requests
import json
import httplib2
ud_data = {'userDefinedData': {"key2": "value2"}}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
http = httplib2.Http()
resp, resp_content = http.request('http://10.12.5.131:30280/api/vnfpkgm/v1/vnf_packages',
    method="POST",
    body=json.dumps(ud_data),
    headers=headers)
print resp['status'], resp_content

