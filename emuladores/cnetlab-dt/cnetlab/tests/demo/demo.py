# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2021 National Network for Education and Research (RNP)        +
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

from cnetlab.dataplane import Dataplane
from cnetlab.log import get_logger
from cnetlab.models.hosts.simplehost import SimpleHost
from cnetlab.models.servers.onos import OnosController
from cnetlab.models.switches.stratum import Stratum
from cnetlab.models.transponders.cassini import Cassini
from cnetlab.models.servers.onosconfig import SendConfigOnos

CONFIG = "ONOS_APPS=gui2,drivers.bmv2,pipelines.fabric,segmentrouting,lldpprovider,hostprovider,proxyarp,openflow,odtn-service,optical-rest,roadm"

PIPECONF_FABRIC = "org.onosproject.pipelines.fabric"


class Topology(Dataplane):

    def nodes(self):
        # Data Center West
        self.add_node("ca1w", Cassini("ca1w"))
        self.add_node("ca2w", Cassini("ca2w"))
        self.add_node("st1w", Stratum("st1w", pipeconf=PIPECONF_FABRIC))
        self.add_node("st2w", Stratum("st2w", pipeconf=PIPECONF_FABRIC))
        self.add_node("st3w", Stratum("st3w", pipeconf=PIPECONF_FABRIC))
        self.add_node("st4w", Stratum("st4w", pipeconf=PIPECONF_FABRIC))
        self.add_node("h1", SimpleHost("h1", ctl=False))
        self.add_node("h2", SimpleHost("h2", ctl=False))
        self.add_node("h3", SimpleHost("h3", ctl=False))
        self.add_node("h4", SimpleHost("h4", ctl=False))

        # Data Center East
        self.add_node("ca1e", Cassini("ca1e"))
        self.add_node("ca2e", Cassini("ca2e"))
        self.add_node("st1e", Stratum("st1e", pipeconf=PIPECONF_FABRIC))
        self.add_node("st2e", Stratum("st2e", pipeconf=PIPECONF_FABRIC))
        self.add_node("st3e", Stratum("st3e", pipeconf=PIPECONF_FABRIC))
        self.add_node("h5", SimpleHost("h5", ctl=False))
        self.add_node("h6", SimpleHost("h6", ctl=False))
        self.add_node("h7", SimpleHost("h7", ctl=False))

    def controller(self):
        self.add_node("ctl1", OnosController("ctl1", onos_app=CONFIG))
        self.get_log("ctl1")
        self.get_terminal("ctl1")

    def set_links(self):
        # OLS Optical Line-Side
        self.add_link("ca1w", "ca1e", mode="opt")
        self.add_link("ca2w", "ca2e", mode="opt")

        # Set West Links
        self.add_link("ca1w", "st1w", mode="eth")
        self.add_link("ca1w", "st2w", mode="eth")
        self.add_link("ca1w", "st3w", mode="eth")
        self.add_link("ca1w", "st4w", mode="eth")

        self.add_link("ca2w", "st1w", mode="eth")
        self.add_link("ca2w", "st2w", mode="eth")
        self.add_link("ca2w", "st3w", mode="eth")
        self.add_link("ca2w", "st4w", mode="eth")

        # Set East Links
        self.add_link("ca1e", "st1e", mode="eth")
        self.add_link("ca1e", "st2e", mode="eth")
        self.add_link("ca1e", "st3e", mode="eth")

        self.add_link("ca2e", "st1e", mode="eth")
        self.add_link("ca2e", "st2e", mode="eth")
        self.add_link("ca2e", "st3e", mode="eth")

        # Hosts West
        ht1_cfg = {'ip': '10.0.1.1', 'cidr': '24', 'gw': '10.0.1.254'}
        self.add_link("h1", "st1w", src_cfg=ht1_cfg)
        ht2_cfg = {'ip': '10.0.2.1', 'cidr': '24', 'gw': '10.0.2.254', 'vlan': 10}
        self.add_link("h2", "st2w", src_cfg=ht2_cfg)
        ht3_cfg = {'ip': '10.0.3.1', 'cidr': '24', 'gw': '10.0.3.254'}
        self.add_link("h3", "st3w", src_cfg=ht3_cfg)
        ht4_cfg = {'ip': '10.0.4.1', 'cidr': '24', 'gw': '10.0.4.254', 'vlan': 20}
        self.add_link("h4", "st4w", src_cfg=ht4_cfg)

        # Host East
        ht5_cfg = {'ip': '10.0.5.1', 'cidr': '24', 'gw': '10.0.5.254'}
        self.add_link("h5", "st1e", src_cfg=ht5_cfg)
        ht6_cfg = {'ip': '10.0.6.1', 'cidr': '24', 'gw': '10.0.6.254', 'vlan': 30}
        self.add_link("h6", "st2e", src_cfg=ht6_cfg)
        ht7_cfg = {'ip': '10.0.7.1', 'cidr': '24', 'gw': '10.0.7.254'}
        self.add_link("h7", "st3e", src_cfg=ht7_cfg)

    def send_config_onos(self):
        def cassini_controller(node, ctl):
            n = self.get_node(node)
            c = self.get_node(ctl)
            n.set_controller(c.ipctl)

        def stratum_controller(node, ctl, **params):
            n = self.get_node(node)
            c = self.get_node(ctl)
            n.set_controller(c.ipctl, **params)

        def send_link(ctl, src, dst, src_port, dst_port, **params):
            c = self.get_node(ctl)
            s = self.get_node(src)
            d = self.get_node(dst)
            config.set_onos_links(c.ipctl, s, d, src_port, dst_port, **params)

        def stratum_interface(ctl, src, host, src_port, gw, cidr, lan, **params):
            c = self.get_node(ctl)
            s = self.get_node(src)
            h = self.get_node(host)
            config.set_stratum_host(c.ipctl, s, h, src_port, gw, cidr, lan, **params)

        cassini_controller('ca1w', 'ctl1')
        cassini_controller('ca2w', 'ctl1')
        cassini_controller('ca1e', 'ctl1')
        cassini_controller('ca2e', 'ctl1')

        stratum_controller('st1w', 'ctl1', sid=100, mac='00:00:00:00:01:00', edge=True)
        stratum_controller('st2w', 'ctl1', sid=200, mac='00:00:00:00:02:00', edge=True)
        stratum_controller('st3w', 'ctl1', sid=300, mac='00:00:00:00:03:00', edge=True)
        stratum_controller('st4w', 'ctl1', sid=400, mac='00:00:00:00:04:00', edge=True)
        stratum_controller('st1e', 'ctl1', sid=500, mac='00:00:00:00:05:00', edge=True)
        stratum_controller('st2e', 'ctl1', sid=600, mac='00:00:00:00:06:00', edge=True)
        stratum_controller('st3e', 'ctl1', sid=700, mac='00:00:00:00:07:00', edge=True)

        # Send OLS Optical Line-Side
        send_link("ctl1", "ca1w", "ca1e", "201", "201", link='OPTICAL')
        send_link("ctl1", "ca2w", "ca2e", "202", "202", link='OPTICAL')

        # Send West Links
        send_link("ctl1", "st1w", "ca1w", "1", "101")
        send_link("ctl1", "st2w", "ca1w", "1", "102")
        send_link("ctl1", "st3w", "ca1w", "1", "103")
        send_link("ctl1", "st4w", "ca1w", "1", "104")

        send_link("ctl1", "st1w", "ca2w", "2", "101")
        send_link("ctl1", "st2w", "ca2w", "2", "102")
        send_link("ctl1", "st3w", "ca2w", "2", "103")
        send_link("ctl1", "st4w", "ca2w", "2", "104")

        # Send East Links
        send_link("ctl1", "st1e", "ca1e", "1", "101")
        send_link("ctl1", "st2e", "ca1e", "1", "102")
        send_link("ctl1", "st3e", "ca1e", "1", "103")

        send_link("ctl1", "st1e", "ca2e", "2", "101")
        send_link("ctl1", "st2e", "ca2e", "2", "102")
        send_link("ctl1", "st3e", "ca2e", "2", "103")

        # Send stratum interfaces
        stratum_interface("ctl1", "st1w", "h1", "3", "10.0.1.254", "24", 10)
        stratum_interface("ctl1", "st2w", "h2", "3", "10.0.2.254", "24", 10, vlan="tagged")
        stratum_interface("ctl1", "st3w", "h3", "3", "10.0.3.254", "24", 20)
        stratum_interface("ctl1", "st4w", "h4", "3", "10.0.4.254", "24", 20, vlan="tagged")

        stratum_interface("ctl1", "st1e", "h5", "3", "10.0.5.254", "24", 30)
        stratum_interface("ctl1", "st2e", "h6", "3", "10.0.6.254", "24", 30, vlan="tagged")
        stratum_interface("ctl1", "st3e", "h7", "3", "10.0.7.254", "24", 40)

    def enable_terminal(self):
        self.get_terminal("ca1w")
        self.get_terminal("ca2w")
        self.get_terminal("ca1e")
        self.get_terminal("ca2e")
        self.get_terminal("st1w")
        self.get_terminal("st2w")
        self.get_terminal("st3w")
        self.get_terminal("st4w")
        self.get_terminal("st1e")
        self.get_terminal("st2e")
        self.get_terminal("st3e")
        self.get_terminal("h1")
        self.get_terminal("h2")
        self.get_terminal("h3")
        self.get_terminal("h4")
        self.get_terminal("h5")
        self.get_terminal("h6")
        self.get_terminal("h7")

    def run(self):
        logger.info("Creating Experiment Cassini-Stratum Network")
        logger.info("Starting Network Controller Into Dataplane")
        logger.info("Starting Onos")
        self.controller()
        logger.info("Starting Nodes Into Dataplane")
        self.nodes()
        logger.info("Starting Links Into Dataplane")
        self.set_links()
        logger.info("Starting terminal experiment")
        self.enable_terminal()
        logger.info("Configuring Equipment and Links into Dataplane")
        self.send_config_onos()


if __name__ == '__main__':
    logger = get_logger(__name__)
    config = SendConfigOnos()

    dp = Topology()

    try:
        dp.run()
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Stopping network emulation")
        dp.delete_all()
