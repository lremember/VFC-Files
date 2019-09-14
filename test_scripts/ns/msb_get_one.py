import requests
resp = requests.get('http://10.12.5.131:30280/api/nsd/v1/ns_descriptors/8acc4e46-08c1-46f3-a594-2910490930de')
print resp.status_code, resp.json()

