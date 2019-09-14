import requests

url = 'http://10.12.5.131:30280/api/vnfpkgm/v1/vnf_packages/3db41499-e3a4-44a4-9a75-f2b028f14589/package_content'
resp = requests.get(url)
local_file = open(r'./vnftest.csar', 'wb')
local_file.write(resp.content)
local_file.close()

