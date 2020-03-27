import requests
import sys

from testscripts.const import MSB_BASE_URL

requests.packages.urllib3.disable_warnings()

resp = requests.delete(MSB_BASE_URL + '/api/nslcm/v1/ns/f1cb0753-4610-4a8a-81e3-fc91ef4d1df0', verify=False)
print(resp.status_code)
