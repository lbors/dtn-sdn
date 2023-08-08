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
import threading

from requests import Session

from cnetlab.dataplane import Dataplane
from cnetlab.log import get_logger
from cnetlab.models.hosts.simplehost import SimpleHost
from cnetlab.models.servers.onos import OnosController
from cnetlab.models.transponders.cassini import Cassini

import time

CONFIG = "ONOS_APPS=netcfglinksprovider,odtn-service,roadm,gui2,optical-rest,hostprovider,fwd"


def send_config(ipctl, json):
    with Session() as s:
        url = "http://{}:8181/onos/v1/network/configuration/".format(ipctl)
        auth = ('karaf', 'karaf')
        s.headers.update({"Content-Type": "application/json"})
        ret = s.post(url=url, auth=auth, data=json)
        if ret.ok:
            logger.info("configuration was sent with successful")
            return True
        else:
            logger.info(ret.content)
            return False


class Topo(Dataplane):

    def create_nodes(self):
        self.add_node('ca1', Cassini('cassini1'))
        self.add_node('ca2', Cassini('cassini2'))
        self.add_node('ht1', SimpleHost('ht1'))
        self.add_node('ht2', SimpleHost('ht2'))
        self.add_node('ctl1', OnosController('ctl1', onos_app=CONFIG))

    def show_terminal(self):
        self.get_terminal('ca2')
        self.get_terminal('ca1')
        self.get_terminal('ht1')
        self.get_terminal('ht2')
        self.get_log('ctl1')
        self.get_log('ca1')
        self.get_log('ca2')



    def create_links(self):
        self.add_link('ca1', 'ca2', mode='opt')
        s_c = {'ip': '10.0.0.1', 'cidr': '24', 'gw': None}
        self.add_link('ht1', 'ca1', mode='eth', src_cfg=s_c)
        d_c = {'ip': '10.0.0.2', 'cidr': '24', 'gw': None}
        self.add_link('ht2', 'ca2', mode='eth', src_cfg=d_c)

    def set_onos_controller(self, node, ctl):
        n = self.get_node(node)
        c = self.get_node(ctl)
        n.set_controller(c.ipctl)

    def gen_link_config(self, src_id, src_port, dst_id, dst_port):
        config = {
            'links' : {
                '{}/{}-{}/{}'.format(src_id, src_port, dst_id,dst_port) : {
                    'basic':{
                        'type': 'OPTICAL',
                        'metric': 1,
                        'durable': True,
                        'bidirectional': True
                    }
                }
            }
        }
        return config.copy()


    def set_onos_links(self, ctl, src, dst, src_port, dst_port):
        def config_link(s, d, i, j):
            exit = False
            logger.info("waiting nodes to configure links")
            while not exit:
                if (s.connected and d.connected):
                    time.sleep(10)
                    logger.info(j)
                    send_config(i, j)
                    exit = True

            logger.info("onos links was configured")

        s = self.get_node(src)
        d = self.get_node(dst)
        c = self.get_node(ctl)

        sid = s.onos_id
        did = d.onos_id

        cfg = self.gen_link_config(sid, src_port, did,dst_port)

        j = json.dumps(cfg, indent=2)

        links = threading.Thread(target=config_link, args=(s, d, c.ipctl, j))
        links.start()

    def run(self):
        logger.info("creating cassini optical transponders")
        self.create_nodes()
        logger.info("cassini transponders were created")
        logger.info("creating optical links")
        self.create_links()
        self.set_onos_controller('ca1', 'ctl1')
        self.set_onos_controller('ca2', 'ctl1')
        logger.info("Show terminal")
        self.show_terminal()
        self.set_onos_links("ctl1", 'ca1', 'ca2', '201', '201')


if __name__ == '__main__':

    logger = get_logger(__name__)

    dp = Topo()

    try:
        dp.run()
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("finishing the network emulation")
        dp.delete_all()
