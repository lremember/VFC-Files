import requests
import json
import httplib2
import sys
inst_id = sys.argv[1]
data = {
    "additionalParamForNs": {
        "sdnControllerId": "2"
    },
    "locationConstraints": [{
        "vnfProfileId": "b1bb0ce7-2222-4fa7-95ed-4840d70a1177",
        "locationConstraints": {
            "vimId": "OCOMP-lcm3_RegionOVP"
        }
    }]
}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
http = httplib2.Http()
resp, resp_content = http.request('http://159.138.133.80:30280/api/nslcm/v1/ns/'+  inst_id + '/instantiate',
    method="POST",
    body=json.dumps(data),
    headers=headers)
print resp['status'], resp_content

