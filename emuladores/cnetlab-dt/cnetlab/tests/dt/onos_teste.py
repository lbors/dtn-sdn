# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2022 National Network for Education and Research (RNP)        +
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

PIPECONF_FABRIC = "org.onosproject.pipelines.fabric"
PIPECONF_BMV2 = "org.onosproject.stratum-pipeconf.bmv2"
CONFIG = [
    "p4runtime",
    "drivers",
    "drivers.bmv2",
    "drivers.p4runtime",
    "drivers.gnoi",
    "drivers.gnmi",
    "pipelines.stratum-bcm",
    "pipelines.fabric",
    "pipelines.basic",
    "route-service",
    "gui2",
    "lldpprovider",
    "hostprovider",
    "proxyarp",
    "segmentrouting",
    "portloadbalancer",
    "mcast",
    "odtn-service",
    "optical-rest",
    "roadm",
    "protocols.gnoi"
]
APPS = "{}={}".format("ONOS_APPS", ",".join(CONFIG))


class Topology(Dataplane):

    def nodes(self):
        # Data Center West
        self.add_node("ca1w", Cassini("ca1w", latitude=45, longitude=-45))
        self.add_node("spine_w1", Stratum("spine_w1", pipeconf=PIPECONF_FABRIC, latitude=15, longitude=-90))
        self.add_node("leaf_w1", Stratum("leaf_w1", pipeconf=PIPECONF_FABRIC, latitude=-30, longitude=-90))
        self.add_node("dtn1", SimpleHost("dtn1", ctl=False))
        # self.add_node("dtn2", SimpleHost("dtn2", ctl=False))

        # Data Center East
        self.add_node("ca1e", Cassini("ca1e", latitude=45, longitude=45))
        self.add_node("spine_e1", Stratum("spine_e1", pipeconf=PIPECONF_FABRIC, latitude=15, longitude=90))
        self.add_node("leaf_e1", Stratum("leaf_e1", pipeconf=PIPECONF_FABRIC, latitude=-30, longitude=90))
        self.add_node("dtn3", SimpleHost("dtn3", ctl=False))
        # self.add_node("dtn4", SimpleHost("dtn4", ctl=False))


    def controller(self):
        self.add_node("ctl1", OnosController("ctl1", onos_app=APPS))
        self.get_log("ctl1")
        self.get_terminal("ctl1")

    def set_links(self):
        # OLS Optical Line-Side
        self.add_link("ca1w", "ca1e", mode="opt")

        # Set West Links
        self.add_link("spine_w1", "ca1w", mode="eth")
        self.add_link("spine_w1", "leaf_w1")

        # Set East Links
        self.add_link("spine_e1", "ca1e", mode="eth")
        self.add_link("spine_e1", "leaf_e1")

        # Hosts West
        dtn1_cfg = {'ip': '10.0.1.1', 'cidr': '24', 'gw': '10.0.1.254'}
        self.add_link("dtn1", "leaf_w1", src_cfg=dtn1_cfg)
        # dtn2_cfg = {'ip': '10.0.1.2', 'cidr': '24', 'gw': '10.0.1.254', 'vlan': 10}
        # self.add_link("dtn2", "leaf_w1", src_cfg=dtn2_cfg)

        # Host East
        dtn3_cfg = {'ip': '10.0.3.1', 'cidr': '24', 'gw': '10.0.3.254'}
        self.add_link("dtn3", "leaf_e1", src_cfg=dtn3_cfg)
        # dtn4_cfg = {'ip': '10.0.3.2', 'cidr': '24', 'gw': '10.0.3.254', 'vlan': 20}
        # self.add_link("dtn4", "leaf_e1", src_cfg=dtn4_cfg)

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
        cassini_controller('ca1e', 'ctl1')

        # West
        stratum_controller('spine_w1', 'ctl1', sid=100, mac='00:00:00:00:01:00')
        stratum_controller('leaf_w1', 'ctl1', sid=110, mac='00:00:00:00:01:10', edge=True)

        # East
        stratum_controller('spine_e1', 'ctl1', sid=300, mac='00:00:00:00:03:00')
        stratum_controller('leaf_e1', 'ctl1', sid=310, mac='00:00:00:00:03:10', edge=True)

        # Send OLS Optical Line-Side
        send_link("ctl1", "ca1w", "ca1e", "201", "201", link='OPTICAL')

        # Send West Links
        send_link("ctl1", "spine_w1", "ca1w", "1", "101", link='INDIRECT')
        send_link("ctl1", "leaf_w1", "spine_w1", "1", "2")

        # Send East Links
        send_link("ctl1", "spine_e1", "ca1e", "1", "101", link='INDIRECT')
        send_link("ctl1", "leaf_e1", "spine_e1", "1", "2")

        send_link("ctl1", "spine_w1", "spine_e1", "1", "1")

        # Send stratum interfaces
        stratum_interface("ctl1", "leaf_w1", "dtn1", "2", "10.0.1.254", "24", 10)
        # stratum_interface("ctl1", "leaf_w1", "dtn2", "3", "10.0.1.254", "24", 10, vlan="tagged")

        stratum_interface("ctl1", "leaf_e1", "dtn3", "2", "10.0.3.254", "24", 20)
        # stratum_interface("ctl1", "leaf_e1", "dtn4", "3", "10.0.3.254", "24", 20, vlan="tagged")




    def enable_terminal(self):
        self.get_terminal("ca1w")
        self.get_terminal("ca1e")
        self.get_terminal("spine_w1")
        self.get_terminal("spine_e1")
        self.get_terminal("leaf_w1")
        self.get_terminal("leaf_e1")
        self.get_terminal("dtn1")
        # self.get_terminal("dtn2")
        self.get_terminal("dtn3")
        # self.get_terminal("dtn4")

    def run(self):
        logger.info("Creating Experiment Cassini-Stratum Network")
        logger.info("Starting Network Controller Into Dataplane")
        logger.info("Starting Onos")
        self.controller()
        logger.info("Starting Nodes Into Dataplane")
        # self.nodes()
        logger.info("Starting Links Into Dataplane")
        # self.set_links()
        logger.info("Starting terminal experiment")
        # self.enable_terminal()
        logger.info("Configuring Equipment and Links into Dataplane")
        # self.send_config_onos()


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
