import requests
import json
import httplib2

data = {
    "context": {
        "globalCustomerId": "ovp-lcm3",
        "serviceType": "tosca_vnf_validation-lcm3"
    },
    "csarId": "b5fb4b55-722b-46b7-9844-9f18be2362db",
    "nsName": "vusn_test5",
    "description": "description"
}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
http = httplib2.Http()
resp, resp_content = http.request('http://159.138.133.80:30280/api/nslcm/v1/ns',
    method="POST",
    body=json.dumps(data),
    headers=headers)
print resp['status'], resp_content

