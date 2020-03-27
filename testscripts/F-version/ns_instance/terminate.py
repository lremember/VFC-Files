import json
import httplib2
import sys

from testscripts.const import MSB_BASE_URL

data = {
    "gracefulTerminationTimeout": 600,
    "terminationType": "FORCEFUL"
}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
ca_certs = None
auth_type = "rest_no_auth"
http = httplib2.Http(ca_certs=ca_certs, disable_ssl_certificate_validation=(auth_type == "rest_no_auth"))
http.follow_all_redirects = True
resp, resp_content = http.request(MSB_BASE_URL + '/api/nslcm/v1/ns/2d5f51a6-7aaf-4a35-9d13-b96cb3cfa08c/terminate',
                                  method="POST",
                                  body=json.dumps(data),
                                  headers=headers)
print(resp['status'], resp_content)
