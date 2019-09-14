import requests

#url = 'http://10.12.5.131:30280/api/nsd/v1/ns_descriptors/a672ce4e-44d6-4331-b25f-1f3acffb985d/nsd_content'
url = 'http://10.12.5.131:30280/api/nsd/v1/ns_descriptors/786593cf-e7d5-4752-b1d0-af6d0bdbc705/nsd_content'
resp = requests.put(url, files={'file': open(r"/home/ubuntu/test/test/ns/ns_vgw.csar", 'rb')})
print resp.status_code

