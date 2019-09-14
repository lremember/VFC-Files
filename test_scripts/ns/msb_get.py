import requests
resp = requests.get('http://159.138.133.80:30280/api/nsd/v1/ns_descriptors')
print resp.status_code, resp.json()

