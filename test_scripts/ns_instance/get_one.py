import requests
resp = requests.get('http://10.12.5.131:30280/api/nslcm/v1/ns/caaed655-8eee-47eb-8649-7fbef4e8fb29')
print resp.status_code, resp.json()
