import requests
import json
import httplib2
import sys
inst_data = sys.argv[1]

data = {
   "gracefulTerminationTimeout": 600, 
   "terminationType": "FORCEFUL"
}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
http = httplib2.Http()
resp, resp_content = http.request('http://10.12.5.131:30280/api/nslcm/v1/ns/' + inst_data + '/terminate',
    method="POST",
    body=json.dumps(data),
    headers=headers)
print resp['status'], resp_content

