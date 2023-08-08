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
import os

from requests.adapters import HTTPAdapter

from cnetlab.node import Node
import cnetlab.log as log

from requests import Session


ONOS_IMAGE = 'onosproject/onos:2.4.0'

logger = log.get_logger(__name__)


def make_req(url, action, auth=None):
    with Session() as r:
        a = HTTPAdapter(max_retries=10)
        r.mount("http://", a)
        resp = None
        if action.__eq__("delete"):
            resp = r.delete(url=url, auth=auth)
        elif action.__eq__("post"):
            resp = r.post(url=url, auth=auth)
        elif action.__eq__("get"):
            resp = r.get(url=url, auth=auth)
        else:
            raise RuntimeError("action not found")
        return resp.ok


def disable_app(addr, app_name):
    url = "http://{addr}:8181/onos/v1/applications/{app}/deactive".format(addr=addr, app=app_name)
    ret = make_req(url, action="delete", auth=('karaf', 'karaf'))
    if not ret:
        raise RuntimeError("cannot enable onos application")


def enable_app(addr, app_name):
    url = "http://{addr}:8181/onos/v1/applications/{app}/active".format(addr=addr, app=app_name)
    ret = make_req(url, action='post', auth=('karaf', 'karaf'))
    if not ret:
        raise RuntimeError("cannot enable onos application")


def test_onos(addr):
    url = "http://{}:8181/onos/v1/docs".format(addr)
    ret = make_req(url, action="get", auth=('karaf', 'karaf'))
    return ret


DEFAULT_CONF = 'ONOS_APPS=gui2,lldpprovider,hostprovider,openflow,proxy,fwd'
DEFAULT_PORTS = {'8181/tcp': 8181,
                 '8101/tcp': 8101,
                 '5005/tcp': 5005,
                 '830/tcp': 830,
                 '9876/tcp': 9876}
DEFAULT_NETWORK = 'bridge'

path = os.getcwd()
CLUSTER_CONF = ['{}/cnetlab/models/servers/cluster.json:/root/onos/config/cluster.json'.format(path)]


class OnosController(Node):
    def __init__(self, name, **kwargs):
        super(OnosController, self).__init__(name, image=ONOS_IMAGE, **kwargs)
        self._onos_app = kwargs.get("onos_app", DEFAULT_CONF)
        self._onos_ports = kwargs.get("onos_ports", DEFAULT_PORTS)
        self._network = kwargs.get("network", DEFAULT_NETWORK)

    def commit(self):
        try:
            config = self.init()
            config.update(environment=['{}'.format(self._onos_app)], ports=self._onos_ports)
            # config.update(environment=['{}'.format(self._onos_app)], ports=self._onos_ports,
            #               volumes=CLUSTER_CONF, network=self._network)
            # config.update(environment=['{}'.format(self._onos_app)])
            self.start(**config)
            logger.info("the onos controller was started")
            logger.info("the controller is available on http://{}:8181/onos/ui/index.html".format(self.ipctl))
        except Exception as ex:
            logger.error(ex)

    def delete(self):
        try:
            self.stop()
            logger.info("the onos controller was deleted")
        except Exception as ex:
            logger.error(ex)
