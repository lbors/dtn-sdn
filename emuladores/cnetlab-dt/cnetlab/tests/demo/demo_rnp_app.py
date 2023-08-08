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
        self.add_node("stratum_w1", Stratum("stratum_w1", pipeconf=PIPECONF_FABRIC, latitude=15, longitude=-90))
        self.add_node("dtn1", SimpleHost("dtn1", ctl=False))

        # Data Center East
        self.add_node("ca1e", Cassini("ca1e", latitude=45, longitude=45))
        self.add_node("stratum_e1", Stratum("stratum_e1", pipeconf=PIPECONF_FABRIC, latitude=15, longitude=90))
        self.add_node("dtn2", SimpleHost("dtn2", ctl=False))


    def controller(self):
        self.add_node("ctl1", OnosController("ctl1", onos_app=APPS))
        self.get_log("ctl1")
        self.get_terminal("ctl1")

    def set_links(self):
        # OLS Optical Line-Side
        self.add_link("ca1w", "ca1e", mode="opt")

        # Set West Links
        self.add_link("stratum_w1", "ca1w", mode="eth")

        # Set East Links
        self.add_link("stratum_e1", "ca1e", mode="eth")

        # Hosts West
        dtn1_cfg = {'ip': '10.0.1.1', 'cidr': '24', 'gw': '10.0.1.254'}
        self.add_link("dtn1", "stratum_w1", src_cfg=dtn1_cfg)

        # Host East
        dtn2_cfg = {'ip': '10.0.2.1', 'cidr': '24', 'gw': '10.0.2.254'}
        self.add_link("dtn2", "stratum_e1", src_cfg=dtn2_cfg)


    def enable_terminal(self):
        self.get_terminal("ca1w")
        self.get_terminal("ca1e")
        self.get_terminal("stratum_w1")
        self.get_terminal("stratum_e1")
        self.get_terminal("dtn1")
        self.get_terminal("dtn2")


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
