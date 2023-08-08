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
import time

from requests import Session

from cnetlab.dataplane import Dataplane
from cnetlab.log import get_logger
from cnetlab.models.hosts.simplehost import SimpleHost
from cnetlab.models.servers.onos import OnosController
from cnetlab.models.switches.stratum import Stratum
from cnetlab.models.transponders.cassini import Cassini

#CONFIG = "ONOS_APPS=netcfglinksprovider,odtn-service,roadm,gui2,optical-rest,hostprovider,fwd,drivers.bmv2,pipelines.fabric,lldpprovider"
CONFIG = "ONOS_APPS=gui2,hostprovider,lldpprovider,proxyarp,openflow,fwd,odtn-service,drivers.bmv2,pipelines.fabric"

PIPECONF_BASIC = "org.onosproject.pipelines.basic"
PIPECONF_FABRIC = "org.onosproject.pipelines.fabric"


class Topology(Dataplane):

    def send_ctl_config(self, ipctl, json):
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


    def set_dp_nodes(self):

        # Data Center West
        self.add_node("ca1w", Cassini("cassini1"))
        self.add_node("st1w", Stratum("st1w", pipeconf=PIPECONF_FABRIC))
        self.add_node("st2w", Stratum("st2w", pipeconf=PIPECONF_FABRIC))
        self.add_node("st3w", Stratum("st3w", pipeconf=PIPECONF_FABRIC))
        self.add_node("dtn1w", SimpleHost("dtn1w"))

        # Data Center East
        self.add_node("ca1e", Cassini("cassini2"))
        self.add_node("st1e", Stratum("st1e", pipeconf=PIPECONF_FABRIC))
        self.add_node("st2e", Stratum("st2e", pipeconf=PIPECONF_FABRIC))
        self.add_node("st3e", Stratum("st3e", pipeconf=PIPECONF_FABRIC))
        self.add_node("dtn1e", SimpleHost("dtn1e"))

    def set_cp_nodes(self):
        self.add_node("ctl1", OnosController('ctl1', onos_app=CONFIG))

    def set_links(self):

        # Set West Links
        # Leaf: st1w, ca1w
        # Spine: st2w, st3w
        self.add_link("st1w", "st2w")
        self.add_link("st1w", "st3w")
        self.add_link("st2w", "ca1w", mode="eth")
        self.add_link("st3w", "ca1w", mode="eth")

        # Set East Links
        # Leaf: st1e, ca1e
        # Spine: st2e, st3e
        self.add_link("st1e", "st2e")
        self.add_link("st1e", "st3e")
        self.add_link("st2e", "ca1e", mode="eth")
        self.add_link("st3e", "ca1e", mode="eth")

        # OLS Optical Line Side
        # West: ca1w
        # East: ca1e
        self.add_link("ca1w", "ca1e", mode='opt')

        # DTN Nodes
        # West
        dtn1w_cfg = {'ip': '10.0.0.1', 'cidr': '24', 'vlan':10}
        self.add_link('dtn1w', 'st1w', src_cfg=dtn1w_cfg)
        # East
        dtn1e_cfg = {'ip': '10.0.0.2', 'cidr': '24', 'vlan':10}
        self.add_link('dtn1e', 'st1e', src_cfg=dtn1e_cfg)

    def config_cassini(self):

        def link_config(src_id, src_port, dst_id, dst_port):
            config = {
                'links': {
                    '{}/{}-{}/{}'.format(src_id, src_port, dst_id, dst_port): {
                        'basic': {
                            'type': 'OPTICAL',
                            'metric': 1,
                            'durable': True,
                            'bidirectional': True
                        }
                    }
                }
            }
            return config.copy()

        def set_onos_links(ctl, src, dst, src_port, dst_port):
            def config_link(s, d, i, j):
                exit = False
                logger.info("waiting nodes to configure links")
                while not exit:
                    if (s.connected and d.connected):
                        time.sleep(10)
                        logger.info(j)
                        self.send_ctl_config(i, j)
                        exit = True

                logger.info("onos links was configured")

            s = self.get_node(src)
            d = self.get_node(dst)
            c = self.get_node(ctl)

            sid = s.onos_id
            did = d.onos_id

            cfg = link_config(sid, src_port, did, dst_port)

            j = json.dumps(cfg, indent=2)

            links = threading.Thread(target=config_link, args=(s, d, c.ipctl, j))
            links.start()

        def set_onos_controller(node, ctl):
            n = self.get_node(node)
            c = self.get_node(ctl)
            n.set_controller(c.ipctl)

        set_onos_controller('ca1w', 'ctl1')
        set_onos_controller('ca1e', 'ctl1')
        set_onos_links("ctl1", "ca1e", "ca1w", "201", "201")



    def config_stratum(self):

        def link_config(src_id, src_port, dst_id, dst_port):
            config = {
                'links': {
                    '{}/{}-{}/{}'.format(src_id, src_port, dst_id, dst_port): {
                        'basic': {
                            'type': 'DIRECT',
                            'metric': 1,
                            'durable': True,
                            'bidirectional': True
                        }
                    }
                }
            }
            return config.copy()

        def set_onos_links(ctl, src, dst, src_port, dst_port):
            def config_link(s, d, i, j):
                exit = False
                logger.info("waiting nodes to configure links")
                while not exit:
                    if (s.connected and d.connected):
                        time.sleep(10)
                        logger.info(j)
                        self.send_ctl_config(i, j)
                        exit = True

                logger.info("onos links was configured")

            s = self.get_node(src)
            d = self.get_node(dst)
            c = self.get_node(ctl)

            sid = s.onos_id
            did = d.onos_id

            cfg = link_config(sid, src_port, did, dst_port)

            j = json.dumps(cfg, indent=2)

            links = threading.Thread(target=config_link, args=(s, d, c.ipctl, j))
            links.start()


        def set_onos_controller(node, ctl):
            n = self.get_node(node)
            c = self.get_node(ctl)
            n.set_controller(c.ipctl)

        set_onos_controller('st1e', 'ctl1')
        set_onos_controller('st2e', 'ctl1')
        set_onos_controller('st3e', 'ctl1')

        set_onos_controller('st1w', 'ctl1')
        set_onos_controller('st2w', 'ctl1')
        set_onos_controller('st3w', 'ctl1')

        set_onos_links("ctl1", "st2w", "ca1w", "2", "101")
        set_onos_links("ctl1", "st3w", "ca1w", "2", "102")
        set_onos_links("ctl1", "st2e", "ca1e", "2", "101")
        set_onos_links("ctl1", "st3e", "ca1e", "2", "102")


    def enable_terminal(self):
        self.get_terminal("ctl1")
        self.get_terminal("ca1e")
        self.get_terminal("ca1w")
        self.get_terminal("dtn1e")
        self.get_terminal("dtn1w")

    def run(self):
        logger.info("Creating Experiment Stratum and Cassini Leaf-Spine Network")
        logger.info("Starting Network Controller Into Dataplane")
        self.set_cp_nodes()
        logger.info("Starting Nodes Into Dataplane")
        self.set_dp_nodes()
        logger.info("Starting Links Into Dataplane")
        self.set_links()
        logger.info("Configuring Cassini Transponders Into Dataplane")
        self.config_cassini()
        logger.info("Configuring Startum Switches  Into Dataplane")
        self.config_stratum()

        self.enable_terminal()

if __name__ == '__main__':

    logger = get_logger(__name__)

    dp = Topology()

    try:
        dp.run()
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Stopping network emulation")
        dp.delete_all()
