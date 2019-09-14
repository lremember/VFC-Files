import requests
import sys

inst_id = sys.argv[1]
resp = requests.delete('http://10.12.5.131:30280/api/nslcm/v1/ns/' + inst_id)

print resp.status_code

