import json
import httplib2

from testscripts.const import MSB_BASE_URL, VNF_PROFILE_ID1, VNF_PROFILE_ID2, VNF_PROFILE_ID3, \
    VNF_PROFILE_ID4, VNF_PROFILE_ID5, VIM_ID

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
    },
    {
        "vnfProfileId": VNF_PROFILE_ID4,
        "locationConstraints": {
            "vimId": VIM_ID
        }
    },
    {
        "vnfProfileId": VNF_PROFILE_ID5,
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
resp, resp_content = http.request(MSB_BASE_URL + '/api/nslcm/v1/ns/79ca0b8b-5294-422f-b034-e057607b0999/instantiate',
                                  method="POST", body=json.dumps(data), headers=headers)
print(resp['status'], resp_content)
