import requests
import sys

from testscripts.const import MSB_BASE_URL


requests.packages.urllib3.disable_warnings()
resp = requests.delete(MSB_BASE_URL + '/api/vnfpkgm/v1/vnf_packages/4b0777cf-036d-4ab2-add6-130ae732f96b', verify=False)
print(resp.status_code)
