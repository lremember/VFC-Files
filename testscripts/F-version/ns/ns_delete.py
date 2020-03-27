import requests
import sys

from testscripts.const import MSB_BASE_URL


requests.packages.urllib3.disable_warnings()
resp = requests.delete(MSB_BASE_URL + '/api/nsd/v1/ns_descriptors/e99de412-9f7f-43d5-ac75-8aaa3de15896', verify=False)
print(resp.status_code)
