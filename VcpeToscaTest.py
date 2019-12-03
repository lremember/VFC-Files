#!/usr/bin/python

# Prerequisites for machine to run this
# Put in required parameters in vcpe_vgw_config.json
# Install python-pip (apt install python-pip)
# Install ONAP CLI
# Must have connectivity to the ONAP, a k8s vm already running is recommended
# Create Preload File, the script will modify the parameters required from serivce model, service instance
# and vnf instance
# Put in CSAR file

import json
import os
import uuid
import requests
import unittest
import time

class VcpeToscaTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def get_out_helper(in_string):
        out_list = (((in_string.replace('-', '')).replace('|', '')).replace('+', '')).split()
        return out_list

    @staticmethod
    def get_out_helper_2(in_string):
        out_list = ((in_string.replace('|', '')).replace('+', '')).split()
        return out_list

    def create_complex(self, config_params):
        complex_create_string = "oclip complex-create -j {} -r {} -x {} -y {} -lt {} -l {} -i {} -lo {} \
                             -S {} -la {} -g {} -w {} -z {} -k {} -o {} -q {} -m {} -u {} -p {}".format(
            config_params["street2"], \
            config_params["physical_location"], config_params["complex_name"], \
            config_params["data_center_code"], config_params["latitude"], config_params["region"], \
            config_params["street1"], config_params["longitude"], config_params["state"], \
            config_params["lata"], config_params["city"], config_params["postal-code"], \
            config_params["complex_name"], config_params["country"], config_params["elevation"], \
            config_params["identity_url"], config_params["aai_url"], config_params["aai_username"], \
            config_params["aai_password"])
        os.system(complex_create_string)

    def delete_complex(self, base_url, header, config_params):
        complex_url = base_url + "/aai/v11/cloud-infrastructure/complexes"
        complex_list_response = requests.get(url=complex_url, headers=header, verify=False)
        if complex_list_response.status_code == 200:
            for complex in (complex_list_response.json())["complex"]:
                if complex['physical-location-id'] == config_params["complex_name"]:
                    complex_version = complex['resource-version']

        if complex_version:
            complex_delete_string = 'oclip complex-delete -x {} -y {} -m {} -u {} -p {}'.format( \
                config_params["complex_name"], complex_version, config_params["aai_url"],
                config_params["aai_username"], config_params["aai_password"])
            os.system(complex_delete_string)
            print("delete complex--successful")

    def register_cloud_helper(self, cloud_region, values, config_params):
        print("Create Cloud--beginning")
        cloud_create_string = 'oclip cloud-create -e {} -b {} -I {{\\\\\\"openstack-region-id\\\\\\":\\\\\\"{}\\\\\\"}} \
           -x {} -y {} -j {} -w {} -l {} -url {} -n {} -q {} -r {} -Q {} -i {} -g {} -z {} -k {} -c {} -m {} -u {} -p {}'.format(
            values.get("esr-system-info-id"), values.get("user-name"), cloud_region, config_params["cloud-owner"], \
            cloud_region, values.get("password"), values.get("cloud-region-version"), values.get("default-tenant"), \
            values.get("service-url"), config_params["complex_name"], values.get("cloud-type"),
            config_params["owner-defined-type"], \
            values.get("system-type"), values.get("identity-url"), config_params["cloud-zone"], values.get("ssl-insecure"), \
            values.get("system-status"), values.get("cloud-domain"), config_params["aai_url"], config_params["aai_username"], \
            config_params["aai_password"])

        os.system(cloud_create_string)
        print("Create Cloud--successful")
        self.cloud_owner = config_params["cloud-owner"]
        self.region_id = cloud_region

        print("Associate Cloud with complex--beginning")
        complex_associate_string = "oclip complex-associate -x {} -y {} -z {} -m {} -u {} -p {}".format(
            config_params["complex_name"], \
            cloud_region, config_params["cloud-owner"], config_params["aai_url"], config_params["aai_username"],
            config_params["aai_password"])
        os.system(complex_associate_string)
        print("Associate Cloud with complex--successful")

        print("Register Cloud with Multicloud--beginning")
        multicloud_register_string = "oclip multicloud-register-cloud -y {} -x {} -m {}".format(
            config_params["cloud-owner"], cloud_region, config_params["multicloud_url"])
        os.system(multicloud_register_string)
        print("Register Cloud with Multicloud--successful")

    def register_all_clouds(self, config_params):
        cloud_dictionary = config_params["cloud_region_data"]
        for cloud_region, cloud_region_values in cloud_dictionary.items():
            VcpeToscaTest().register_cloud_helper(cloud_region, cloud_region_values, config_params)

    def delete_cloud_helper(self, base_url, header, config_params):
        print("Multicloud-cloud-delete--beginning")
        cloud_region = list(config_params["cloud_region_data"].keys())[0]
        multicloud_delete_string = "oclip multicloud-cloud-delete -y {} -x {} -m {}".format(
            config_params["cloud-owner"], cloud_region, config_params["multicloud_url"])
        os.system(multicloud_delete_string)
        print("Multicloud-cloud-delete----successful")

        print("Disassociate Cloud with complex--beginning")
        complex_disassociate_string = "oclip complex-disassociate -x {} -y {} -z {} -m {} -u {} -p {}".format(
            self.config_params["complex_name"],
            cloud_region, config_params["cloud-owner"], config_params["aai_url"],
            config_params["aai_username"],
            config_params["aai_password"])
        os.system(complex_disassociate_string)
        print("Disassociate Cloud with complex--successful")

        print("Delete Cloud--beginning")
        cloud_list_url = base_url + "/aai/v11/cloud-infrastructure/cloud-regions"
        cloud_list_response = requests.get(url=cloud_list_url, headers=header, verify=False)
        if cloud_list_response.status_code == 200:
            for cloud in (cloud_list_response.json())["cloud-region"]:
                if cloud['cloud-region-id'] == cloud_region:
                    cloud_version = cloud['resource-version']

        if cloud_version:
            service_delete_string = 'oclip cloud-delete -x {} -y {} -m {} -u {} -p {}'.format(
                config_params["cloud-owner"], cloud_region, cloud_version, config_params["aai_url"],
                config_params["aai_username"], config_params["aai_password"])
            os.system(service_delete_string)
            print("delete service type--successful")

    def create_service_type(self, config_params):
        create_string = "oclip service-type-create -x {} -y {} -m {} -u {} -p {}".format(
            config_params["service_name"], config_params["service_name"], config_params["aai_url"],
            config_params["aai_username"], config_params["aai_password"])
        os.system(create_string)

    def delete_service_tpe(self, base_url, header, config_params):
        print("delete service type--beginning")
        service_tpe_list_url = base_url + "/aai/v11/service-design-and-creation/services"
        service_type_list_response = requests.get(url=service_tpe_list_url, headers=header, verify=False)
        if service_type_list_response.status_code == 200:
            for service in (service_type_list_response.json())["service"]:
                if service["service-id"] == config_params["service_name"]:
                    service_type_version = service['resource-version']

        if service_type_version:
            service_delete_string = 'oclip service-type-delete -x {} -y {} -m {} -u {} -p {}'.format(
                config_params["service_name"], service_type_version, config_params["aai_url"],
                config_params["aai_username"], config_params["aai_password"])
            os.system(service_delete_string)
            print("delete service type--successful")

    def create_customer(self, config_params):
        create_string = "oclip customer-create -x {} -y {} -m {} -u {} -p {}".format(config_params["customer_name"], \
                                                                                     config_params["subscriber_name"],
                                                                                     config_params["aai_url"],
                                                                                     config_params["aai_username"],
                                                                                     config_params["aai_password"])
        os.system(create_string)

    def create_tenant(self, config_params):
        cloud_region_id = list(config_params["cloud_region_data"].keys())[0]
        tenant_id = config_params["cloud_region_data"][cloud_region_id]["tenant-id"]
        tenant_name = config_params["cloud_region_data"][cloud_region_id].get("default-tenant")
        create_tenant = "oclip tenant-create -x {} -y {} -z {} -r {} -m {} -u {} -p {}".format(config_params["cloud-owner"],
                                                                                     cloud_region_id, tenant_id,
                                                                                     tenant_name,
                                                                                     config_params["aai_url"],
                                                                                     config_params["aai_username"],
                                                                                     config_params["aai_password"])
        os.system(create_tenant)
        print("create tenant successfully.")

    def delete_customer(self, base_url, header, config_params):
        print("delete customer--beginning")
        customer_list_url = base_url + "/aai/v11/business/customers"
        customer_list_response = requests.get(url=customer_list_url, headers=header, verify=False)
        if customer_list_response.status_code == 200:
            for cutsomer in (customer_list_response.json())["customer"]:
                if cutsomer['global-customer-id'] == config_params["customer_name"]:
                    customer_version = cutsomer['resource-version']

        if customer_version:
            customer_delete_string = 'oclip customer-delete -x {} -y {} -m {} -u {} -p {}'.format(
                config_params["customer_name"], customer_version, config_params["aai_url"],
                config_params["aai_username"], config_params["aai_password"])
            os.system(customer_delete_string)
            print("delete customer--successful")

    def add_customer_subscription(self, config_params):
        subscription_check = 0
        for cloud_region, cloud_region_values in (config_params["cloud_region_data"]).items():
            if subscription_check == 0:
                subscription_string = "oclip subscription-create -x {} -c {} -z {} -e {} -y {} -r {} -m {} -u {} -p {}".format(
                    config_params["customer_name"], cloud_region_values.get("tenant-id"), config_params["cloud-owner"],
                    config_params["service_name"],
                    cloud_region_values.get("default-tenant"), cloud_region, config_params["aai_url"],
                    config_params["aai_username"], config_params["aai_password"])
            else:
                subscription_string = "oclip subscription-cloud-add -x {} -c {} -z {} -e {} -y {} -r {} -m {} -u {} -p {}".format(
                    config_params["customer_name"], cloud_region_values.get("tenant-id"), config_params["cloud-owner"],
                    config_params["service_name"],
                    cloud_region_values.get("default-tenant"), cloud_region, config_params["aai_url"],
                    config_params["aai_username"], config_params["aai_password"])
            os.system(subscription_string)
            subscription_check += 1

    def remove_customer_subscription(self, base_url, header, config_params):
        print("remove subscription--beginning")
        customer_subscription_url = base_url + "/aai/v11/business/customers/customer/%s/service-subscriptions" % self.global_customer_id
        resp = requests.get(url=customer_subscription_url, headers=header, verify=False)
        if resp.status_code == 200:
            for subscription in (resp.json())["service-subscription"]:
                if subscription['service-type'] == config_params["service_name"]:
                    subscription_version = subscription['resource-version']

        if subscription_version:
            subscription_delete_string = 'oclip subscription-delete -x {} -y {} -g {} -m {} -u {} -p {}'.format(
                config_params["customer_name"], config_params["service_name"], subscription_version, config_params["aai_url"],
                config_params["aai_username"], config_params["aai_password"])
            os.system(subscription_delete_string)
            print("delete subscription--successful")

    def register_vnfm_helper(self, vnfm_key, values, config_params):
        print("Create vnfm--beginning")
        esr_vnfm_id = str(uuid.uuid4())
        vnfm_create_string = 'oclip vnfm-create -b {} -c {} -e {} -v {} -g {} -x {} -y {} -i {} -j {} -q {} \
        -m {} -u {} -p {}'.format(vnfm_key, values.get("type"), values.get("vendor"), \
                                  values.get("version"), values.get("url"), values.get("vim-id"), esr_vnfm_id, \
                                  values.get("user-name"), values.get("user-password"), values.get("vnfm-version"), \
                                  config_params["aai_url"], config_params["aai_username"], config_params["aai_password"])

        os.system(vnfm_create_string)
        print("Create vnfm--successful")
        return esr_vnfm_id

    def register_vnfm(self, config_params):
        vnfm_params = config_params["vnfm_params"]
        for vnfm_key, vnfm_values in vnfm_params.items():
             return VcpeToscaTest().register_vnfm_helper(vnfm_key, vnfm_values, config_params)

    def unregister_vnfm(self, base_url, header, esr_vnfm_id, config_params):
        print("delete vnfm--beginning")
        vnfm_url = base_url + "aai/v11/external-system/esr-vnfm-list"
        resp = requests.get(url=vnfm_url, headers=header, verify=False)
        if resp.status_code == 200:
            for vnfm in (resp.json())["esr-vnfm"]:
                if vnfm['vnfm-id'] == esr_vnfm_id:
                    esr_vnfm_version = vnfm['resource-version']

        if esr_vnfm_id and esr_vnfm_version:
            vnfm_delete_string = 'oclip vnfm-delete -x {} -y {} -m {} -u {} -p {}'.format( \
                esr_vnfm_id, esr_vnfm_version, config_params["aai_url"], \
                config_params["aai_username"], config_params["aai_password"])
            os.system(vnfm_delete_string)
            print("delete vnfm--successful")

    def create_ns(self, base_url, config_params, csar_id):
        ns = config_params["ns"]
        # ns_create_string = 'oclip 。sh -m {} -c {} -n {} -q {} -S {}'.format(config_params["vfc-url"], \
        #                                                                                  csar_id, ns.get("name"),
        #                                                                                  config_params["customer_name"],
        #                                                                                  config_params["service_name"])
        # print(ns_create_string)
        # ns_create_out = (os.popen(ns_create_string)).read()
        # print(ns_create_out)
        # ns_instance_id = (VcpeToscaTest.get_out_helper_2(ns_create_out))[4]
        data = {
            "context": {
                "globalCustomerId": config_params["customer_name"],
                "serviceType": config_params["service_name"]
            },
            "csarId": csar_id,
            "nsName": ns.get("name"),
            "description": "description"
        }
        ns_header = {'content-type': 'application/json', 'accept': 'application/json'}
        ns_url = base_url + "/api/nslcm/v1/ns"
        ns_resp = requests.post(ns_url, data=json.dumps(data), headers=ns_header)
        print(ns_resp.status_code)
        if 201 == ns_resp.status_code:
            ns_instance_id = ns_resp.json().get("nsInstanceId")
            print(ns_resp.status_code, ns_resp.json())
            print("create ns successfully, the ns instance id is %s" % ns_instance_id)
            return ns_instance_id
        else:
            return ""

    def instantiate_ns(self, base_url, ns_instance_id, vnfdId, config_params):
        print("Instantiate ns beginning")
        # ns_instantiate_string = 'oclip vfc-nslcm-instantiate -m {} -i {} -c {} -n {}'.format(
        #     config_params["vfc-url"], ns_instance_id, config_params["location"], config_params["sdc-controller-id"])
        # print(ns_instantiate_string)
        #
        # ns_instantiate_out = (os.popen(ns_instantiate_string)).read()
        # print(ns_instantiate_out)
        # ns_instance_jod_id = (VcpeToscaTest.get_out_helper_2(ns_instantiate_out))[3]

        data = {
            "additionalParamForNs": {
                "sdncontroller": config_params["sdc-controller-id"],
            },
            "locationConstraints": [
                {
                    "vnfProfileId": vnfdId,
                    "locationConstraints": {
                        "vimId": config_params["location"]
                    }
                }
            ]
        }

        header = {'content-type': 'application/json', 'accept': 'application/json'}
        instance_url = base_url + "/api/nslcm/v1/ns/" + ns_instance_id + "/instantiate"
        instance_resp = requests.post(instance_url, data=json.dumps(data), headers=header)
        print(instance_resp.status_code, instance_resp.json())
        if 200 == instance_resp.status_code:
            ns_instance_jod_id = instance_resp.json().get("jobId")
            print("Instantiate ns successfully, the job id is %s" % ns_instance_jod_id)
            return ns_instance_jod_id
        else:
            print("Instantiate ns failed.")
            return ""

    def create_ns_package(self, base_url, config_params):
        print("Create ns package is beginning")
        ns = config_params["ns"]
        ns_url = base_url + "/api/nsd/v1/ns_descriptors"
        ns_headers = {'content-type': 'application/json', 'accept': 'application/json'}
        ns_data = {'userDefinedData': {ns.get("key"): ns.get("value")}}
        ns_package_reps = requests.post(ns_url, data=json.dumps(ns_data), headers=ns_headers)
        print(ns_package_reps.status_code)
        if 201 == ns_package_reps.status_code:
            print("Create ns package successful, the ns package id is %s" % (ns_package_reps.json()["id"]))
            return ns_package_reps.json()["id"]
        else:
            return ""

    def create_vnf_package(self, base_url, config_params):
        print("Create vnf package is beginning")
        vnfs = config_params["vnfs"]
        vnf_url = base_url + "/api/vnfpkgm/v1/vnf_packages"
        #vnf_url = "http://192.168.235.41:30280/api/vnfpkgm/v1/vnf_packages"
        header = {'content-type': 'application/json', 'accept': 'application/json'}
        for vnf_key, vnf_values in vnfs.items():
            vnf_data = {'userDefinedData': {vnf_values.get("key"): vnf_values.get("value")}}
            vnf_package_reps = requests.post(vnf_url, data=json.dumps(vnf_data), headers=header)
            print(vnf_package_reps.status_code)
            if 201 == vnf_package_reps.status_code:
                print("Create vnf package successful, the vnf package id is %s" % (vnf_package_reps.json()["id"]))
                return vnf_package_reps.json()["id"]
        return ""

    def upload_ns_package(self, ns_package_id, config_params):
        ns = config_params["ns"]
        header = {'accept': 'application/json'}
        ns_upload_url = '{}/api/nsd/v1/ns_descriptors/{}/nsd_content'.format(config_params["vfc-url"],
                                                                                ns_package_id)
        print(ns_upload_url)
        file_path = os.path.dirname(os.path.abspath(__file__))
        ns_vgw = file_path + "/" + ns["path"]
        print(ns_vgw)
        ns_file = open(ns_vgw, 'rb')
        print(ns_file)
        for i in range(10):
            resp = requests.put(ns_upload_url, files={'file': ns_file})
            if 204 == resp.status_code:
                break
            else:
                time.sleep(1)
        ns_file.close()
        return resp

    def upload_vnf_package(self, vnf_package_id, config_params):
        vnfs = config_params["vnfs"]
        for vnf_key, vnf_values in vnfs.items():
            vnf_upload_url = '{}/api/vnfpkgm/v1/vnf_packages/{}/package_content'.format(config_params["vfc-url"],
                                                                                        vnf_package_id)
            print(vnf_upload_url)
            file_path = os.path.dirname(os.path.abspath(__file__))
            vgw = file_path + "/" + vnf_values.get("path")
            vnf_file = open(vgw, 'rb')
            print(vnf_file)
            for i in range(10):
                resp = requests.put(vnf_upload_url, files={'file': vnf_file})
                print(resp.status_code)
                if 202 == resp.status_code:
                    break
                else:
                    time.sleep(1)
            vnf_file.close()

    def get_vnf_package(self, base_url, vnf_package_id, config_params):
        vnf_package_url = base_url + '/api/vnfpkgm/v1/vnf_packages/%s' % vnf_package_id
        vnf_resp = requests.get(vnf_package_url)
        if 200 == vnf_resp.status_code:
            vnfdId = vnf_resp.json().get("vnfdId")
            print("vnfdId is %s" % vnfdId)
            return vnfdId
        else:
            return ""

    @staticmethod
    def getVnf(vnfs):
        for vnf in vnfs:
            if 'relationship-list' in vnf:
                for relation in vnf["relationship-list"]["relationship"]:
                    if "service-instance" == relation["related-to"]:
                        if "ns_123" in relation["related-link"]:
                            return vnf
        return ""

    def findVserver(vnf):
        if 'relationship-list' in vnf:
            for relation in vnf["relationship-list"]["relationship"]:
                if "vserver" == relation["related-to"]:
                    for relationData in relation["relationship-data"]:
                        if "vserver.vserver-id" == relationData["relationship-key"]:
                            return relationData["relationship-value"]
        return ""

    def waitProcessFinished(self, base_url, job_id, ns_instance_id, action):
        print("Wait for the %s ns finished." % action)
        job_url = base_url + "/api/nslcm/v1/jobs/%s" % job_id
        for i in range(20):
            job_resp = requests.get(url=job_url)
            print(job_resp.status_code)
            if 200 == job_resp.status_code:
                process = (job_resp.json())["responseDescriptor"]["progress"]
                if 100 != process:
                    print("Ns %s %s started. The process is %s." % (ns_instance_id, action, process))
                    time.sleep(1)
                else:
                    print("Ns %s %s successfully." % (ns_instance_id, action))
                    break

    def testNs(self):
        base_url = "http://msb-iag:80"
        file_path = os.path.dirname(os.path.abspath(__file__))
        f = open(file_path + "//vcpe_config_1.json")
        config_params = json.load(f)
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'X-TransactionId': "9999",
            'Real-Time': "true",
            'X-FromAppId': "jimmy-postman",
            "Authorization": "Basic QUFJOkFBSQ=="
        }
        print("Set cli command environment--beginning")
        os.environ["OPEN_CLI_PRODUCT_IN_USE"] = config_params["open_cli_product"]
        os.environ["OPEN_CLI_HOME"] = config_params["open_cli_home"]
        print("Set cli command environment--successful")

        print("Create cloud complex--beginning")
        VcpeToscaTest().create_complex(config_params)
        print("Create cloud complex--successful")

        print("Register all clouds--beginning")
        VcpeToscaTest().register_all_clouds(config_params)
        print("Register all clouds--successful")

        print("create vCPE service")
        VcpeToscaTest().create_service_type(config_params)

        print("create customer")
        VcpeToscaTest().create_customer(config_params)

        print("create tenant")
        VcpeToscaTest().create_tenant(config_params)

        print("add customer and subscription")
        VcpeToscaTest().add_customer_subscription(config_params)

        print("Register vnfm")
        esr_vnfm_id = VcpeToscaTest().register_vnfm(config_params)
        # 5.create csar file
        # 5.1 upload csar file to catalog
        # 5.2 FIXME:Because SDC internal API will change without notice, so I will maually design VNF and Service.
        # SDC output data model is not align with VFC, we use an workaround method
        # We just do run time automation
        ns_package_id = ""
        print("Use csar file is uploaded by local")
        vnf_package_id = VcpeToscaTest().create_vnf_package(base_url, config_params)
        self.assertIsNotNone(vnf_package_id)

        ns_package_id = VcpeToscaTest().create_ns_package(base_url, config_params)
        self.assertIsNotNone(ns_package_id)

        print("Upload vnf package from csar beginning")
        VcpeToscaTest().upload_vnf_package(vnf_package_id, config_params)
        print("Upload vnf package from csar successfully")

        print("Get vnfdId.")
        vnfdId = VcpeToscaTest().get_vnf_package(base_url, vnf_package_id, config_params)

        print("Upload ns package from csar beginning")
        ns_out = VcpeToscaTest().upload_ns_package(ns_package_id, config_params)
        print(ns_out)
        print("Upload ns package from csar successfully")

        # 7. VFC part
        print("Create ns beginning")
        ns_instance_id = VcpeToscaTest().create_ns(base_url, config_params, ns_package_id)
        print(ns_instance_id)
        self.assertIsNotNone(ns_instance_id)

        ns_instance_jod_id = VcpeToscaTest().instantiate_ns(base_url, ns_instance_id, vnfdId, config_params)
        self.assertIsNotNone(ns_instance_jod_id)

        VcpeToscaTest().waitProcessFinished(base_url, ns_instance_jod_id, ns_instance_id, "instantiate")

        vnf_aai_url = base_url + "/aai/v11/network/generic-vnfs"
        vnf_resp = requests.get(url=vnf_aai_url, headers=header, verify=False)
        self.assertEqual(200, vnf_resp.status_code)

        vnfs = vnf_resp.json()["generic-vnf"]
        print(vnf_resp.json())
        vnf = VcpeToscaTest().getVnf(vnfs)
        vnf_id = vnf["vnf-id"]
        print("Create vnf %s successfully." % vnf_id)

        vserver_id = VcpeToscaTest().findVserver(vnf)
        print(list(config_params["cloud_region_data"].keys())[0])
        print(config_params["cloud_region_data"].values())

        cloud_region_id = list(config_params["cloud_region_data"].keys())[0]
        tenant_id = config_params["cloud_region_data"][cloud_region_id]["tenant-id"]
        vserver_aai_url = base_url + "/aai/v11/cloud-infrastructure/cloud-regions/cloud-region/%s/" \
               "%s/tenants/tenant/%s/vservers/vserver/%s?depth=all" % \
               (config_params["cloud-owner"], cloud_region_id, tenant_id, vserver_id)

        vserver_resp = requests.get(url=vserver_aai_url, headers=header, verify=False)
        self.assertEqual(200, vserver_resp.status_code)
        print("Create vserver %s successfully." % vserver_id)

        if ns_instance_id:
            print("terminate ns--beginning")
            ns_url = base_url + "/api/nslcm/v1/ns/%s" % ns_instance_id
            d = {
                "gracefulTerminationTimeout": 600,
                "terminationType": "FORCEFUL"
            }
            res = requests.post(ns_url, data=d)
            self.assertEquals(200, res.status_code)
            terminate_ns_job_id = res.json()["jobId"]
            VcpeToscaTest().waitProcessFinished(terminate_ns_job_id, "terminate")

            print("delete ns--beginning")
            res = requests.delete(ns_url)
            self.assertEquals(200, res.status_code)

        f.close()

        print("Delete vnfm %s" % esr_vnfm_id)
        VcpeToscaTest().unregister_vnfm(base_url, header, esr_vnfm_id, config_params)

        print("Remove service subscription")
        VcpeToscaTest().remove_customer_subscription(base_url, header, config_params)

        print("Remove customer %s" % config_params["customer_name"])
        VcpeToscaTest().delete_customer(base_url, header, config_params)

        print("Remove service type %s" % config_params["service_name"])
        VcpeToscaTest().delete_service_tpe(base_url, header, config_params)

        print("Remove cloud %s" % config_params["cloud-owner"])
        VcpeToscaTest().delete_cloud_helper(base_url, header, config_params)

        print("Remove complex %s" % config_params["complex_name"])
        VcpeToscaTest().delete_complex(base_url, header, config_params)

        f.close()
