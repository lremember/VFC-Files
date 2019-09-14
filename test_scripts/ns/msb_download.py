import requests
url = 'http://10.12.5.131:30280/api/nsd/v1/ns_descriptors/2db88cc0-c72a-4e1d-9036-368b3a465697/nsd_content'
resp = requests.get(url)
local_file = open(r'./dns.csar', 'wb')
local_file.write(resp.content)
local_file.close()

