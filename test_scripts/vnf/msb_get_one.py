import requests
#resp = requests.get('http://172.30.3.104:30280/api/vnfpkgm/v1/vnf_packages/396b889f-529f-426a-97ab-65b00720b308')
resp = requests.get('http://10.12.5.131:30280/api/catalog/v1/vnfpackages/ed8e7818-31a0-4527-a732-15089fb22bee')
print resp.status_code, resp.json()

