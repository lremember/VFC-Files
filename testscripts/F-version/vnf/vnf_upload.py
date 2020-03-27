import requests
import sys

from testscripts.const import MSB_BASE_URL, VNF_CSAR_PATH5


requests.packages.urllib3.disable_warnings()
url = MSB_BASE_URL + '/api/vnfpkgm/v1/vnf_packages/84dc8fdb-2395-4a4c-9ff8-ef942cf96bde/package_content'
resp = requests.put(url, files={'file': open(VNF_CSAR_PATH5, 'rb')}, verify=False)
print(resp.status_code)
