import requests
resp = requests.get('http://159.138.133.80:30280/api/vnfpkgm/v1/vnf_packages')
print resp.status_code, resp.json()

