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
import threading
import time

from requests import Session

from cnetlab.node import Node
from cnetlab.ovsdb import OVSCTL
from cnetlab.networkconfig import VethNetworkConfig, FibreNetworkConfig
from cnetlab.models.servers.onosconfig import SendConfigOnos

logger = logging.getLogger(__name__)

NETCONF_PORT = "830"

class Cassini(Node):
    def __init__(self, name, **params):

        super().__init__(name, image="sdnm/cassini-sdnm:latest")
        self._ovsctl = OVSCTL(self)
        self._eth_net_config = VethNetworkConfig(netns=name, **params)
        self._opt_net_config = FibreNetworkConfig(netns=name, **params)
        self._latitude = params.get('latitude', None)
        self._longitude = params.get('longitude', None)
        self._connected = False
        self._onos_id = None
        self._config = SendConfigOnos()
        self._network = params.get('network', None)

    @property
    def running(self):
        return self._ovsctl.exist_port("xe16")

    @property
    def connected(self):
        return self._connected

    @property
    def onos_id(self):
        return self._onos_id

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
    def network(self):
        return self._network

    @network.setter
    def network(self, value):
        self._network = value

    def commit(self):
        conf = self.init()
        conf.update(volumes={'/lib/modules': {'bind': '/lib/modules', 'mode': 'rw'}},
                    network='{}'.format('bridge' if self.network is None else self.network))
        self.start(**conf)
        logger.info("starting transponder sdnm-cassini {}".format(self.name))
        while True:
            if self.running:
                logger.info("the processes in {} have started".format(self.name))
                break
            time.sleep(5)
        self._onos_id = "netconf:{}:{}".format(self.ipctl, NETCONF_PORT)
        logger.info("the cassini transponder {} has started".format(self.name))

    def delete(self):
        logger.info("stopping transponder sdnm-cassini {}".format(self.name))
        try:
            self.stop()
            logger.info("the cassini transponder {} was deleted".format(self.name))
        except Exception as ex:
            logger.error(ex)

    def get_port(self, **params):
        mode = params.get("mode")
        if mode.__eq__('eth'):
            return self._eth_net_config.get_port()
        elif mode.__eq__('opt'):
            return self._opt_net_config.get_port()
        else:
            raise IndexError("only 'eth' and 'opt' mode are supported")

    def add_port(self, **params):
        try:

            name = params['name']
            mode = params['mode']
            if mode.__eq__('eth'):
                self._eth_net_config.add_port(**params)
                prefix = self._eth_net_config.prefix
                idx = name.split('-')[1].replace(prefix, "")
                br = "xe{}".format(idx)
                self._ovsctl.add_if_bridge(bridge=br, port=name)
                logger.info("new port ({}) was attached to ethernet channel {}".format(name, br))
            elif mode.__eq__('opt'):
                self._opt_net_config.add_port(**params)
                prefix = self._opt_net_config.prefix
                idx = name.split('-')[1].replace(prefix, "")
                br = "oe{}".format(idx)
                self._ovsctl.add_if_bridge(bridge=br, port=name)
                logger.info("new port ({}) was attached to optical channel {}".format(name, br))
            else:
                raise RuntimeError("mode is not supported")
        except Exception as ex:
            logger.error(ex)

    def rem_port(self, **params):

        try:
            name = params['name']
            m = name.split('-')[1]
            if m.startswith('opt'):
                mode = 'opt'
            elif m.startswith('vif'):
                mode = 'eth'
            else:
                raise RuntimeError("mode was not found")

            if mode.__eq__("eth"):
                prefix = self._eth_net_config.prefix
                idx = name.split('-')[1].replace(prefix, "")
                br = "xe{}".format(idx)
                self._ovsctl.rem_if_bridge(bridge=br, port=name)
                self._eth_net_config.rem_port(name=name)
            elif mode.__eq__("opt"):
                prefix = self._opt_net_config.prefix
                idx = name.split('-')[1].replace(prefix, "")
                br = "oe{}".format(idx)
                self._ovsctl.rem_if_bridge(bridge=br, port=name)
                self._opt_net_config.rem_port(name=name)
            else:
                logger.error("the port type was not found")

        except Exception as ex:
            logger.error(ex)

    def set_controller(self, ipctl):

        mods = [
            'org.onosproject.models.openconfig-odtn',
            'org.onosproject.models.openconfig',
            'org.onosproject.models.ietf',
            'org.onosproject.models.tapi',
            'org.onosproject.drivers.odtn-driver',
            'org.onosproject.drivers.netconf',
            'org.onosproject.drivers.optical',
            'org.onosproject.protocols.restconfserver',
            'org.onosproject.odtn-service',
            'org.onosproject.netcfglinksprovider',
            'org.onosproject.generaldeviceprovider',
            'org.onosproject.configsync-netconf',
            'org.onosproject.netconf',
            'org.onosproject.yang',
            'org.onosproject.odtn-api',
            'org.onosproject.roadm',
            'org.onosproject.restsb',
            'org.onosproject.restconf',
            'org.onosproject.optical-rest',
            'org.onosproject.optical-model'
        ]

        def connect_onos(i, m):
            devices = self.gen_device_config()
            j = json.dumps(devices, indent=2)
            self._config.modules_is_running(i, m)
            logger.info(j)
            ret = self._config.send_ctl_config(i, j)
            if ret:
                self._connected = True

        try:
            logger.info("connecting {} to onos".format(self.name))
            dev = threading.Thread(target=connect_onos, args=(ipctl, mods))
            dev.start()
            logger.info("{} connect to onos".format(self.name))
        except Exception as ex:
            logger.error(ex)

    def gen_device_config(self):
        config = {
            'devices': {
                '{}'.format(self.onos_id): {
                    'basic': {
                        'name': self.name,
                        'driver': 'cassini-openconfig',
                        "longitude": self.longitude,
                        "latitude": self.latitude
                    },
                    'netconf': {
                        'ip': self.ipctl,
                        'port': NETCONF_PORT,
                        'username': 'root',
                        'password': 'root',
                        "idle-timeout": "0"
                    }
                }
            }
        }

        return config.copy()
