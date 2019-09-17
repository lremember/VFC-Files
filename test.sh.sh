set -ex

MULTICLOUD_PLUGIN_ENDPOINT=http://192.168.2.61:30280/api/multicloud/v0/CloudOwner_RegionOne
TOKEN=$(curl -v -s -H "Content-Type: application/json" -X POST -d '{ }'  $MULTICLOUD_PLUGIN_ENDPOINT/identity/v3/auth/tokens 2>&1 | grep X-Subject-Token | sed "s/\r//g" | sed "s/^.*: //" |  cat -v)
PROJECT_ID=$(curl -v -s  -H "Content-Type: application/json" -H "X-Auth-Token: $TOKEN" -X GET $MULTICLOUD_PLUGIN_ENDPOINT/identity/v3/projects 2>/dev/null | python -mjson.tool | grep -B5 "name.*\"admin" | grep '\"id\"' | cut -f4 -d'"')
curl -v -s  -H "Content-Type: application/json" -H "X-Auth-Token: $TOKEN" -X GET $MULTICLOUD_PLUGIN_ENDPOINT/identity/v3/projects/$PROJECT_ID
curl -v -s  -H "Content-Type: application/json" -H "X-Auth-Token: $TOKEN" -X GET $MULTICLOUD_PLUGIN_ENDPOINT/compute/v2.1/$PROJECT_ID/flavors