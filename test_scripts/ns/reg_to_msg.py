import requests
import json
import httplib2
ud_data = {"serviceName": "aai-externalSystem", "version": "v11", "url": "/aai/v11/external-system","protocol": "REST", "enable_ssl":"false", "lb_policy":"ip_hash", "nodes": [ {"ip": "10.12.5.131","port": "30233"}]}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
http = httplib2.Http()
resp, resp_content = http.request('http://msb-iag:80/api/microservices/v1/services',
    method="POST",
    body=json.dumps(ud_data),
    headers=headers)
print resp['status'], resp_content

