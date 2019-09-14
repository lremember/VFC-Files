import requests
resp = requests.delete('http://10.12.5.131:30280/api/nsd/v1/ns_descriptors/28243652-98f1-4d51-998a-abf71c53db47')
print resp.status_code

