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
from cnetlab.models.servers.onosconfig import SendConfigOnos

CONFIG = "ONOS_APPS=gui2,drivers.bmv2,pipelines.fabric,segmentrouting,lldpprovider,hostprovider,proxyarp,openflow,odtn-service,optical-rest,roadm"

PIPECONF_FABRIC = "org.onosproject.pipelines.fabric"


class Topology(Dataplane):

    def set_nodes(self):
        # Cassini basic topology with Stratum bmv2 Trellis

        # Transponders
        self.add_node("ca1", Cassini("ca1"))
        self.add_node("ca2", Cassini("ca2"))

        # Stratum
        self.add_node("st1", Stratum("st1", pipeconf=PIPECONF_FABRIC))
        self.add_node("st2", Stratum("st2", pipeconf=PIPECONF_FABRIC))

        # Nodes
        self.add_node("h1", SimpleHost("h1", ctl=False))
        # self.add_node("h2", SimpleHost("h2", ctl=False))
        self.add_node("h3", SimpleHost("h3", ctl=False))
        # self.add_node("h4", SimpleHost("h4", ctl=False))

        # Nodes Opticos
        self.add_node("op1", SimpleHost("op1", ctl=False))
        self.add_node("op2", SimpleHost("op2", ctl=False))

    def set_control(self):
        self.add_node("ctl1", OnosController("ctl1", onos_app=CONFIG))
        self.get_log("ctl1")
        self.get_terminal("ctl1")

    def set_links(self):
        self.add_link("st1", "ca1", mode="eth")
        self.add_link("st2", "ca2", mode="eth")
        self.add_link("ca1", "ca2", mode="opt")
        self.add_link("ca1", "ca2", mode="opt")

        # Hosts
        ht1_cfg = {'ip': '10.0.2.1', 'cidr': '24', 'gw': '10.0.2.254'}
        self.add_link("h1", "st1", src_cfg=ht1_cfg)
        # ht2_cfg = {'ip': '10.0.2.2', 'cidr': '24', 'gw': '10.0.2.254', 'vlan': 10}
        # self.add_link("h2", "st1", src_cfg=ht2_cfg)
        ht3_cfg = {'ip': '10.0.2.2', 'cidr': '24', 'gw': '10.0.2.254'}
        self.add_link("h3", "st2", src_cfg=ht3_cfg)
        # ht4_cfg = {'ip': '10.0.3.2', 'cidr': '24', 'gw': '10.0.3.254', 'vlan': 20}
        # self.add_link("h4", "st2", src_cfg=ht4_cfg)

        op1_cfg = {'ip': '10.0.4.1', 'cidr': '24', 'gw': '10.0.4.254'}
        self.add_link('op1', 'ca1', mode='eth', src_cfg=op1_cfg)
        op2_cfg = {'ip': '10.0.4.2', 'cidr': '24', 'gw': '10.0.4.254'}
        self.add_link('op2', 'ca2', mode='eth', src_cfg=op2_cfg)

    def send_config_onos(self):
        def set_cassini_to_controller(node, ctl):
            n = self.get_node(node)
            c = self.get_node(ctl)
            n.set_controller(c.ipctl)

        def set_stratum_to_controller(node, ctl, **params):
            n = self.get_node(node)
            c = self.get_node(ctl)
            n.set_controller(c.ipctl, **params)

        def set_link(ctl, src, dst, src_port, dst_port, **params):
            c = self.get_node(ctl)
            s = self.get_node(src)
            d = self.get_node(dst)
            conf.set_onos_links(c.ipctl, s, d, src_port, dst_port, **params)

        def stratum_interface(ctl, src, host, src_port, gw, cidr, lan, **params):
            c = self.get_node(ctl)
            s = self.get_node(src)
            h = self.get_node(host)
            conf.set_stratum_host(c.ipctl, s, h, src_port, gw, cidr, lan, **params)

        set_cassini_to_controller('ca1', 'ctl1')
        set_cassini_to_controller('ca2', 'ctl1')

        set_stratum_to_controller('st1', 'ctl1', sid=100, mac='00:00:00:00:01:00', edge=True)
        set_stratum_to_controller('st2', 'ctl1', sid=200, mac='00:00:00:00:02:00', edge=True)

        set_link("ctl1", "ca1", "ca2", "201", "201", link='OPTICAL')
        set_link("ctl1", "ca1", "ca2", "202", "202", link='OPTICAL')
        set_link("ctl1", "st1", "ca1", "1", "101")
        set_link("ctl1", "st2", "ca2", "1", "101")

        stratum_interface("ctl1", "st1", "h1", "2", "10.0.2.254", "24", 10)
        # stratum_interface("ctl1", "st1", "h2", "3", "10.0.2.254", "24", 10, vlan="tagged")
        stratum_interface("ctl1", "st2", "h3", "2", "10.0.2.254", "24", 20)
        # stratum_interface("ctl1", "st2", "h4", "3", "10.0.3.254", "24", 20, vlan="tagged")

    def enable_terminal(self):
        self.get_terminal("ca1")
        self.get_terminal("ca2")
        self.get_terminal("st1")
        self.get_terminal("st2")
        self.get_terminal("h1")
        # self.get_terminal("h2")
        self.get_terminal("h3")
        # self.get_terminal("h4")

        self.get_terminal("op1")
        self.get_terminal("op2")

    def run(self):
        logger.info("Creating Experiment Cassini-Stratum Network")
        logger.info("Starting Network Controller Into Dataplane")
        logger.info("Starting Onos")
        self.set_control()
        logger.info("Starting Nodes Into Dataplane")
        self.set_nodes()
        logger.info("Starting Links Into Dataplane")
        self.set_links()
        logger.info("Starting terminal experiment")
        self.enable_terminal()
        logger.info("Configuring Equipment and Links into Dataplane")
        self.send_config_onos()


if __name__ == '__main__':

    logger = get_logger(__name__)
    conf = SendConfigOnos()

    dp = Topology()

    try:
        dp.run()
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Stopping network emulation")
        dp.delete_all()
