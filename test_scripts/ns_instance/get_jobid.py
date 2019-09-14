import requests
import sys
jobId = '1'
if len(sys.argv) > 1:
    jobId = sys.argv[1]
resp = requests.get('http://10.12.5.131:30280/api/nslcm/v1/jobs/%s' % jobId)
print resp.status_code, resp.json()
