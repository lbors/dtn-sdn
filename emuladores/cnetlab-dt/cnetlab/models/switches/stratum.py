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

import json
import logging
import socket
import threading
import time

from cnetlab.iproute import IPR
from cnetlab.node import Node
from cnetlab.networkconfig import VethNetworkConfig
from cnetlab.models.servers.onosconfig import SendConfigOnos

logger = logging.getLogger(__name__)


class Stratum(Node):
    def __init__(self, name, nodeid=1, **params):
        super().__init__(name, image="sdnm/stratum:latest", **params)
        self._veth_net_config = VethNetworkConfig(netns=name)
        self._latitude = params.get('latitude', None)
        self._longitude = params.get('longitude', None)
        self._pipeconf = params.get('pipeconf', 'org.onosproject.pipelines.basic')
        self._driver = params.get('driver', 'stratum-bmv2')
        self._ipr = IPR(netns=name)
        self._nodeid = nodeid
        self._onos_id = "device:{}"
        self._connected = True
        self._config = SendConfigOnos()
        self._network = params.get('network', None)

    @property
    def driver(self):
        return self._driver

    @property
    def pipeconf(self):
        return self._pipeconf

    @pipeconf.setter
    def pipeconf(self, value):
        self._pipeconf = value

    @property
    def nodeid(self):
        return self._nodeid

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    @property
    def onos_id(self):
        return self._onos_id.format(self.name)

    @property
    def connected(self):
        return self._connected

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, value):
        self._network = value

    def commit(self):
        try:
            conf = self.init()
            conf.update(environment=["LONGITUDE={}".format(('null' if self.longitude is None else self.longitude)),
                                     "LATITUDE={}".format(('null' if self.latitude is None else self.latitude)),
                                     "NODEID={}".format(self.nodeid)],
                        network='{}'.format('bridge' if self.network is None else self.network))
            self.start(**conf)
            while True:
                a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                location = (self.ipctl, 50001)
                result = a_socket.connect_ex(location)
                if result == 0:
                    logger.info("the processes in {} have started".format(self.name))
                    break
                else:
                    time.sleep(2)
            logger.info("the stratum switch ({}) was started".format(self.name))
        except Exception as ex:
            logger.error(ex)

            return True

    def get_port(self, **params):
        try:
            return self._veth_net_config.get_port()
        except Exception as ex:
            logger.error(ex)

    def add_port(self, **params):
        try:

            name = params['name']
            self._veth_net_config.add_port(**params)
            prefix = self._veth_net_config.prefix
            idx = name.split('-')[1].replace(prefix, "")
            bridge = "port{}".format(idx)
            self._ipr.set_if_bridge(bridge, name)
            logger.info("the interface {} was  attached to port {} of switch {}".format(name, bridge, self.name))
        except Exception as ex:
            logger.error(ex)

    def rem_port(self, **params):
        try:
            name = params['name']
            prefix = self._veth_net_config.prefix
            idx = name.split('-')[1].replace(prefix, "")
            bridge = "port{}".format(idx)
            self._ipr.rem_if_bridge(name)
            self._ipr.set_del(name)
            logger.info("the interface {} was removed from port {} in switch {}".format(name, bridge, self.name))
        except Exception as ex:
            logger.error(ex)

    def gen_config(self):

        config = {
            'devices': {
                'device:{}'.format(self.name): {
                    'basic': {
                        "managementAddress": "grpc://{}:50001?device_id={}".format(self.ipctl, self.nodeid),
                        "driver": "{}".format(self.driver),
                        "pipeconf": "{}".format(self.pipeconf),
                        "longitude": self.longitude,
                        "latitude": self.latitude
                    }
                }
            }
        }
        return config.copy()

    def gen_fabric_config(self, sid, mac, edge):

        config = {
            'devices': {
                'device:{}'.format(self.name): {
                    'basic': {
                        "managementAddress": "grpc://{}:50001?device_id={}".format(self.ipctl, self.nodeid),
                        "driver": "{}".format(self.driver),
                        "pipeconf": "{}".format(self.pipeconf),
                        "longitude": self.longitude,
                        "latitude": self.latitude
                    },
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

    def set_controller(self, ip_ctl, **params):
        mods = [
            "org.onosproject.drivers.stratum",
            "org.onosproject.pipelines.fabric",
            "org.onosproject.drivers.gnmi",
            "org.onosproject.protocols.grpc",
            "org.onosproject.generaldeviceprovider",
            "org.onosproject.drivers.odtn-driver",
            "org.onosproject.drivers.p4runtime",
            "org.onosproject.pipelines.basic",
            "org.onosproject.drivers.gnoi",
            "org.onosproject.drivers.bmv2"
        ]

        def connect_onos():

            if self.pipeconf == 'org.onosproject.pipelines.basic':
                devices = self.gen_config()

            else:
                sid = params.get('sid', None)
                mac = params.get('mac', None)
                edge = params.get('edge', False)

                devices = self.gen_fabric_config(sid, mac, edge)

            j = json.dumps(devices, indent=2)
            logger.info(j)
            self._config.modules_is_running(ip_ctl, mods)
            self._config.send_ctl_config(ip_ctl, j)
            self._connected = True

        try:
            logger.info("connecting {} to onos".format(self.name))
            dev = threading.Thread(target=connect_onos)
            dev.start()
            logger.info("{} connect to onos".format(self.name))
        except Exception as ex:
            logger.error(ex)

    def delete(self):
        self.stop()
        logger.info("stratum switch {} was deleted".format(self.name))
