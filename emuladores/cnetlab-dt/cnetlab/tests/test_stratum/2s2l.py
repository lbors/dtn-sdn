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

# import json
# import threading
# import time
#
# from requests import Session

from cnetlab.dataplane import Dataplane
from cnetlab.log import get_logger
from cnetlab.models.hosts.simplehost import SimpleHost
from cnetlab.models.servers.onos import OnosController
from cnetlab.models.switches.stratum import Stratum

CONFIG = "ONOS_APPS=gui,drivers.bmv2,pipelines.fabric,segmentrouting,lldpprovider,hostprovider"

PIPECONF_FABRIC = "org.onosproject.pipelines.fabric"

class Topology(Dataplane):

    def set_nodes(self):
        
        # Para carregar a topologia no onos, abra um novo terminal e acesse o diretório 
        # do arquivo s2l2_topo.json, por fim, execute o comando a seguir:
        # curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.17.0.10:8181/onos/v1/network/configuration/ -d@2s2l_topo.json

        # Trellis basic topology

        # Switches
        self.add_node("spine1", Stratum("spine1", pipeconf=PIPECONF_FABRIC))
        self.add_node("spine2", Stratum("spine2", pipeconf=PIPECONF_FABRIC))
        self.add_node("leaf1", Stratum("leaf1", pipeconf=PIPECONF_FABRIC))
        self.add_node("leaf2", Stratum("leaf2", pipeconf=PIPECONF_FABRIC))

        # Nodes
        self.add_node("h1", SimpleHost("h1", ctl=False))
        self.add_node("h2", SimpleHost("h2", ctl=False))
        self.add_node("h3", SimpleHost("h3", ctl=False))
        self.add_node("h4", SimpleHost("h4", ctl=False))

    def set_control(self):
        self.add_node("ctl1", OnosController("ctl1", onos_app=CONFIG))
        self.get_log("ctl1")
        self.get_terminal("ctl1")

    def set_links(self):
        self.add_link("spine1", "leaf1")
        self.add_link("spine1", "leaf2")
        self.add_link("spine2", "leaf1")
        self.add_link("spine2", "leaf2")

        # Hosts
        ht1_cfg = {'mac': '00:aa:00:00:00:01', 'ip': '10.0.2.1', 'cidr': '24'}
        self.add_link("h1", "leaf1", src_cfg=ht1_cfg)
        ht2_cfg = {'mac': '00:aa:00:00:00:02', 'ip': '10.0.2.2', 'cidr': '24', 'vlan': 10}
        self.add_link("h2", "leaf1", src_cfg=ht2_cfg)
        ht3_cfg = {'mac': '00:aa:00:00:00:03', 'ip': '10.0.3.1', 'cidr': '24'}
        self.add_link("h3", "leaf2", src_cfg=ht3_cfg)
        ht4_cfg = {'mac': '00:aa:00:00:00:04', 'ip': '10.0.3.2', 'cidr': '24', 'vlan': 20}
        self.add_link("h4", "leaf2", src_cfg=ht4_cfg)

    def enable_terminal(self):
        self.get_terminal("spine1")
        self.get_log("spine1")
        self.get_terminal("spine2")
        self.get_terminal("leaf1")
        self.get_terminal("leaf2")
        self.get_terminal("h1")
        self.get_terminal("h2")
        self.get_terminal("h3")
        self.get_terminal("h4")

    def run(self):
        logger.info("Creating Experiment Stratum Leaf-Spine Network")
        logger.info("Starting Network Controller Into Dataplane")
        self.set_nodes()
        logger.info("Starting Onos")
        self.set_control()
        logger.info("Starting Links Into Dataplane")
        self.set_links()

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
