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

import logging
from collections import deque

from cnetlab.iproute import IPR

logger = logging.getLogger(__name__)


def gen_ports_queue(prefix, max):
    l = []
    for i in range(1, max):
        l.append("{}{}".format(prefix, i))

    q = deque(l)
    return q.copy()

class NetworkConfig(object):
    def __init__(self, netns, **params):
        self._netns = netns

    def get_port(self, **params):
        pass

    def add_port(self, **params):
        pass

    def rem_port(self, **params):
        pass

class HostNetworkConfig(NetworkConfig):
    def __init__(self, netns, **params):
        super().__init__(netns, **params)
        self._kind = params.get('kind', 'host')
        self._prefix = "{}-{}".format(netns,  params.get('prefix', 'ht'))
        self._ports = gen_ports_queue(self._prefix, 10)
        self._ipr = IPR(netns)

    @property
    def kind(self):
        return self._kind

    @property
    def prefix(self):
        return self._prefix

    def get_port(self, **params):
        if len(self._ports) > 0:
            return self._ports.popleft()
        else:
            raise IndexError("there are not ports available")

    def add_port(self, **params):
        name = params.get("name", None)
        assert name is not None, "the port name cannot be null"

        config = params.get('config')

        try:
            self._ipr.set_if_ns(name)
            self._ipr.set_up(name)
            self._ipr.set_mtu(name, 9000)

            if len(config) > 0:
                vid = config.get('vlan', None)
                ipaddr = config.get('ip', None)
                cidr = config.get('cidr', None)
                gate = config.get('gw', None)
                mac =  config.get('mac', None)

                if vid is not None:
                    name = self._ipr.set_if_vlan(name, vid)
                    self._ipr.set_up(name)
                    self._ipr.set_mtu(name, 9000)

                if ipaddr is not None:
                    self._ipr.set_address(name, ipaddr, cidr, gate)

                if mac is not None:
                    self._ipr.set_mac(name, mac)

        except Exception as ex:
            raise RuntimeError(ex)


    def rem_port(self, **params):
        name = params.get('name', None)
        assert name is not None, "the port name cannot be null"
        try:
            self._ports.appendleft(name)
            self._ipr.set_del(name)
        except Exception as ex:
            raise RuntimeError("the port {} cannot be deleted: {}".format(name, ex))


class VethNetworkConfig(NetworkConfig):
    def __init__(self, netns, **params):
        super().__init__(netns, **params)
        self._kind = params.get('kind', 'veth')
        self._prefix = params.get('prefix', 'vif')
        self._ifname = "{}-{}".format(netns, self.prefix)
        self._ipr = IPR(netns)
        self._ports = gen_ports_queue(self.ifname, 80)

    @property
    def kind(self):
        return self._kind

    @property
    def prefix(self):
        return self._prefix

    @property
    def ifname(self):
        return self._ifname

    def get_port(self, **params):
        if len(self._ports) > 0:
            return self._ports.popleft()
        else:
            raise IndexError("there are not ports available")

    def add_port(self, **params):
        name = params.get('name', None)
        assert name is not None, "the port name cannot be null"
        try:
            self._ipr.set_if_ns(name)
            self._ipr.set_up(name)
            self._ipr.set_mtu(name, mtu=9000)
        except Exception as ex:
            raise RuntimeError(ex)


    def rem_port(self, **params):
        name = params.get('name', None)
        assert name is not None, "the port name cannot be null"
        try:
            self._ports.appendleft(name)
            self._ipr.set_del(name)
        except Exception as ex:
            raise RuntimeError("the port {} cannot be deleted: {}".format(name, ex))

class FibreNetworkConfig(VethNetworkConfig):
    def __init__(self, netns, **params):
        super().__init__(netns, prefix='ovif', **params)
