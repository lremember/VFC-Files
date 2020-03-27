import requests
import sys
from testscripts.const import MSB_BASE_URL, NS_CSAR_PATH

requests.packages.urllib3.disable_warnings()
url = MSB_BASE_URL + '/api/nsd/v1/ns_descriptors/35364096-c0c7-4d6e-abf6-9267e4b40508/nsd_content'
resp = requests.put(url, files={'file': open(NS_CSAR_PATH, 'rb')}, verify=False)
print(resp.status_code)
