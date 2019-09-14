import requests
resp = requests.get('http://10.12.5.131:30280/api/nslcm/v1/ns')
print resp.status_code, resp.json()
