# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2020 National Network for Education and Research (RNP)        +
#                                                                              +
#     Licensed under the Apache License, Version 2.0 (the "License");          +
#     you may not use this file except in compliance with the License.         +
#     You may obtain a copy of the License at                                  +
#                                                                              +
#         http://www.apache.org/licenses/LICENSE-2.0                           +
#                                                                              +
#     Unless required by applicable law or agreed to in writing, software      +
#     distributed under the License is distributed on an "AS IS" BASIS,        +
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. +
#     See the License for the specific language governing permissions and      +
#     limitations under the License.                                           +
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from cnetlab.node import Node


class OVSCTL(object):

    def __init__(self, node: Node):
        self.node = node

    @property
    def running(self):
        cmd = "ovs-vsctl get Open_vSwitch . ovs_version"
        try:
            self.__run_cmd(cmd)
            return True
        except Exception:
            return False

    def __run_cmd(self, cmd) -> str:
        ret, out = self.node.exec_cmd(cmd)
        if ret != 0:
            raise RuntimeError(out)
        else:
            return out.decode().replace('\r\n', ' ').strip()

    def exist_port(self, name):
        cmd = "ovs-vsctl br-exists {}".format(name)
        try:
            self.__run_cmd(cmd)
            return True
        except Exception as ex:
            return False

    def add_bridge(self, name):
        cmd = "ovs-vsctl add-br {}".format(name)
        self.__run_cmd(cmd)

    def rem_bridge(self, name):
        cmd = "ovs-vsctl del-br {}".format(name)
        self.__run_cmd(cmd)

    def add_if_bridge(self, bridge, port):
        cmd = "ovs-vsctl add-port {} {}".format(bridge, port)
        self.__run_cmd(cmd)

    def rem_if_bridge(self, bridge, port):
        cmd = "ovs-vsctl del-port {} {}".format(bridge, port)
        self.__run_cmd(cmd)

    def list_if_bridge(self, bridge):
        cmd = "ovs-vsctl list-ports {}".format(bridge)
        ret = self.__run_cmd(cmd)
        ports = ret.split()
        return ports.copy()

    def get_if_tags(self, port):
        cmd = "ovs-vsctl get port {} tag".format(port)
        tag = self.__run_cmd(cmd)
        if tag.__eq__("[]"):
            return None
        return tag

    def get_if_trunk(self, port):
        cmd = "ovs-vsctl get port {} trunks".format(port)
        ret = self.__run_cmd(cmd)
        trunks = ret.split(",")
        if trunks.__eq__("[]"):
            return None
        return trunks

    def set_if_tag(self, port, tag: str):
        cmd = "ovs-vsctl set port {} tag={}".format(port, tag)
        self.__run_cmd(cmd)

    def set_if_trunk(self, port, trunk: list):
        cmd = "ovs-vsctl set port {} trunks={}".format(port, ",".join(trunk))
        self.__run_cmd(cmd)

    def set_of_controller(self, bridge, addr, port):
        cmd = "ovs-vsctl set-controller {} tcp:{}:{}".format(bridge, addr, port)
        self.__run_cmd(cmd)

    def set_of_version(self, bridge, protocol):
        cmd = "ovs-vsctl set bridge {} protocols={}".format(bridge, ",".join(protocol))
        self.__run_cmd(cmd)

    def set_of_dpdi(self, bridge, dpdi):
        cmd = "ovs-vsctl set bridge {} other-config:datapath-id={}".format(bridge, dpdi)
        self.__run_cmd(cmd)