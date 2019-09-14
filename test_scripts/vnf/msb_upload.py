import requests
#url = 'http://10.12.5.131:30280/api/vnfpkgm/v1/vnf_packages/0703ad1f-346f-4bfe-ae26-831593fcc2a4/package_content'
url = 'http://10.12.5.131:30280/api/vnfpkgm/v1/vnf_packages/cd08ce44-f205-414d-a8b2-68b4aa0ea184/package_content'
resp = requests.put(url, files={'file': open(r"/home/ubuntu/test/test/vnf/vgw.csar", 'rb')})
print resp.status_code

