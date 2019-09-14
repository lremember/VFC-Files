import requests
resp = requests.delete('http://159.138.133.80:30280/api/vnfpkgm/v1/vnf_packages/aee7b0d7-1b3b-47f9-a6ed-7d4c495a152c')
print resp.status_code

