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

from cnetlab.node import Node
from cnetlab.networkconfig import HostNetworkConfig
from cnetlab.iproute import IPR

logger = logging.getLogger(__name__)


class SimpleHost(Node):
    def __init__(self, name, ctl=True):
        super().__init__(name, image="sdnm/simplehost:latest")
        self._net_config = HostNetworkConfig(netns=name, kind='veth')
        self._ctl_net = ctl
        self._ipr = IPR(netns=name)
        self._connected = True

    @property
    def connected(self):
        return self._connected

    def _enable_offload(self, ifname):
        type = ['rx', 'tx', 'sg']
        for t in type:
            cmd = "ethtool --offload {} {} off".format(ifname, t)
            exit, out = self.exec_cmd(cmd)
            if exit != 0:
                raise RuntimeError(out)

    def commit(self):
        conf = self.init()
        if not self._ctl_net:
            conf.update(network_disabled=True)

        self.start(**conf)
        logger.info("the simple host ({}) was started".format(self.name))

    def delete(self):
        self.stop()
        logger.info("the simple host ({}) was deleted".format(self.name))

    def get_port(self, **params):
        try:
            return self._net_config.get_port()
        except Exception as ex:
            logger.error(ex)

    def add_port(self, **params):
        try:
            self._net_config.add_port(**params)
            self._enable_offload(params['name'])
        except Exception as ex:
            logger.error(ex)

    def rem_port(self, **params):
        try:
            self._net_config.rem_port(**params)
        except Exception as ex:
            logger.warning(ex)

    def set_route(self, dst_net, gateway):
        try:
           self._ipr.set_route(dst_net, gateway)
        except Exception as ex:
            logger.error(ex)
