import json
import httplib2
import sys

from testscripts.const import VNF_PROFILE_ID1, VIM_ID, MSB_BASE_URL, VNF_PROFILE_ID2, VNF_PROFILE_ID3, \
    NS_INST_ID

data = {
    "additionalParamForNs": {
        "sdnControllerId": "2"
    },
    "locationConstraints": [{
        "vnfProfileId": VNF_PROFILE_ID1,
        "locationConstraints": {
            "vimId": VIM_ID
        }
    },
    {
        "vnfProfileId": VNF_PROFILE_ID2,
        "locationConstraints": {
            "vimId": VIM_ID
        }
    },
    {
        "vnfProfileId": VNF_PROFILE_ID3,
        "locationConstraints": {
            "vimId": VIM_ID
        }
    }]

}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
ca_certs = None
auth_type = "rest_no_auth"
http = httplib2.Http(ca_certs=ca_certs, disable_ssl_certificate_validation=(auth_type == "rest_no_auth"))
http.follow_all_redirects = True
resp, resp_content = http.request(MSB_BASE_URL + '/api/nslcm/v1/ns/' + NS_INST_ID +'/instantiate',
                                  method="POST", body=json.dumps(data), headers=headers)
print(resp['status'], resp_content)
