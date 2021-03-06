# Copyright (c) 2019, CMCC Technologies Co., Ltd.
# Copyright (c) 2019, ZTE Corporation.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from rest_framework import serializers

from lcm.ns.enum import CHANGE_TYPE, CHANGE_RESULT
from lcm.pub.utils.enumutil import enum_to_list
from lcm.ns.serializers.sol.ext_virtual_link_info import ExtVirtualLinkInfoSerializer
from lcm.ns.serializers.sol.update_serializers import ModifyVnfInfoDataSerializer


class ChangedInfoSerializer(serializers.Serializer):
    changedVnfInfo = ModifyVnfInfoDataSerializer(
        help_text="Information about the changed VNF instance information, including configurable properties",
        required=False)
    changedExtConnectivity = serializers.ListField(
        child=ExtVirtualLinkInfoSerializer(),
        help_text="Link to the task resource that represents the 'fail' Information about changed external "
                  "connectivity, if applicable.",
        required=False)


class AffectedVnfsSerializer(serializers.Serializer):
    vnfInstanceId = serializers.UUIDField(
        help_text="Identifier of the VNF instance.",
        required=True
    )
    vnfdId = serializers.UUIDField(
        help_text="Identifier of the VNFD of the VNF Instance.",
        required=True
    )
    vnfProfileId = serializers.UUIDField(
        help_text="Identifier of the VNF profile of the NSD.",
        required=True
    )
    vnfName = serializers.CharField(
        help_text="Name of the VNF Instance.",
        required=True)
    changeType = serializers.ChoiceField(
        help_text="Signals the type of change",
        required=True,
        choices=enum_to_list(CHANGE_TYPE)
    )
    changeResult = serializers.ChoiceField(
        help_text="Signals the result of change identified by the 'changeType' attribute.",
        required=True,
        choices=enum_to_list(CHANGE_RESULT)
    )
    changedInfo = ChangedInfoSerializer(
        help_text="Information about the changed VNF instance information, including VNF configurable properties, if applicable.",
        required=False)
