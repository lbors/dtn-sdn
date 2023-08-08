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

import itertools
import logging
import random
import time
import uuid
import json
import threading

from cnetlab.node import Node
from cnetlab.ovsdb import OVSCTL as ovs
from cnetlab.networkconfig import VethNetworkConfig
from cnetlab.models.servers.onosconfig import SendConfigOnos

logger = logging.getLogger(__name__)

def gen_dpdi():
    import uuid
    return "0000{}".format(str(uuid.uuid4()).replace("-","")[:12])

class Whitebox(Node):
    def __init__(self, name, dpid=None):
        super().__init__(name, image="sdnm/whitebox:latest")
        self._ovsctl = ovs(self)
        self._veth_net_config = VethNetworkConfig(netns=name)
        self._dpid = (dpid if dpid is not None else gen_dpdi())
        self._connected = False
        self._config = SendConfigOnos()

    @property
    def br(self):
        return "br0"

    @property
    def onos_id(self):
        return "of:{}".format(self.dpid)

    @property
    def connected(self):
        return self._connected

    @property
    def dpid(self):
        if len(self._dpid) == 16 :
            return self._dpid
        else:
            raise IndexError("dpid must have 16 bits")
    def commit(self):
        try:
            conf = self.init()
            conf.update(volumes={'/lib/modules': {'bind': '/lib/modules', 'mode': 'rw'}},)
            self.start(**conf)
            while True:
                if self._ovsctl.running:
                    logger.info("the processes in {} have started".format(self.name))
                    break
                time.sleep(2)
            self.add_bridge(self.br)
            logger.info("whitebox ({}) was started".format(self.name))
        except Exception as ex:
            logger.error(ex)

    def delete(self):
        try:
            self.stop()
            logger.info("whitebox ({}) was deleted".format(self.name))
        except Exception as ex:
            logger.error(ex)

    def add_bridge(self, name, protocol=None):
        if protocol is None:
            protocol = ["OpenFlow13"]
        try:
            self._ovsctl.add_bridge(name)
            self._ovsctl.set_of_version(name,protocol)
            self._ovsctl.set_of_dpdi(name, self.dpid)
        except Exception as ex:
            logger.error(ex)

    def rem_bridge(self, name):
        try:
            self._ovsctl.rem_bridge(name)
        except Exception as ex:
            logger.error(ex)

    def get_port(self, **params):
        try:
            return self._veth_net_config.get_port()
        except Exception as ex:
            logger.error(ex)

    def add_port(self, **params):
        try:
            self._veth_net_config.add_port(**params)
            self._ovsctl.add_if_bridge(self.br, params['name'])
            logger.info("the port {} was attached to {}".format(params['name'], self.name))
        except Exception as ex:
            logger.error(ex)

    def rem_port(self, **params):

        try:
            self._ovsctl.rem_if_bridge(self.br, params['name'])
            self._veth_net_config.rem_port(name=params['name'])
            logger.info("the port {} was remove from {}".format(params['name'], self.name))
        except Exception as ex:
            logger.warning(ex)

    def gen_fabric_config(self, sid, mac, edge):
        config = {
            'devices': {
                "basic": {
                    "name": "{}".format(self.name)
                },
                'of:{}'.format(self.dpid): {
                    'segmentrouting': {
                        'name': '{}'.format(self.name),
                        'ipv4NodeSid': sid,
                        'ipv4Loopback': '{}'.format(self.ipctl),
                        'routerMac': '{}'.format(mac),
                        'isEdgeRouter': edge,
                        'adjacencySids': []
                    }
                }
            }
        }
        return config.copy()

    def set_controller(self, ipctl, port, **params):
        routing = params.get('seg', None)

        try:
            logger.info("connecting {} to onos".format(self.name))
            self._ovsctl.set_of_controller(self.br, ipctl, port)
            if routing:
                sid = params.get('sid', None)
                mac = params.get('mac', None)
                edge = params.get('edge', False)
                devices = self.gen_fabric_config(sid, mac, edge)
                j = json.dumps(devices, indent=2)
                self._config.send_ctl_config(ipctl, j)
                logger.info("{} connect to onos".format(self.name))

            self._connected = True
        except Exception as ex:
            logger.error(ex)
