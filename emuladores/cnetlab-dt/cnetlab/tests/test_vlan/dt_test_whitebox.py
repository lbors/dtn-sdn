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

import cnetlab.log as log
from cnetlab.dataplane import Dataplane
from cnetlab.models.hosts.simplehost import SimpleHost
from cnetlab.models.servers.onos import OnosController
from cnetlab.models.switches.whitebox import Whitebox


class Topo(Dataplane):

    def create_nodes(self):
        self.add_node("sw1", Whitebox("sw1"))
        self.add_node("sw2", Whitebox("sw2"))
        self.add_node("ht1", SimpleHost("ht1"))
        self.add_node("ht2", SimpleHost("ht2"))
        self.add_node("ht3", SimpleHost("ht3"))
        self.add_node("ctl1", OnosController("ctl1"))

    def create_links(self):
        self.add_link(src="sw1", dst="sw2")
        self.add_link(src="sw1", dst="sw2")
        self.add_link(src="ht1", dst="sw1", src_cfg={'ip': '10.0.1.1', 'cidr': '24', 'gw': None})
        self.add_link(src="ht2", dst="sw2", src_cfg={'ip': '10.0.2.1', 'cidr': '24', 'gw': None})
        self.add_link(src="ht3", dst="sw2", src_cfg={'ip': '10.0.3.1', 'cidr': '24', 'gw': None})
        

    def configure_controller(self):
        ctl1 = self.get_node("ctl1")
        sw2 = self.get_node("sw2")
        sw2.set_controller(ctl1.ipctl, 6653)
        sw1 = self.get_node("sw1")
        sw1.set_controller(ctl1.ipctl, 6653)

    # def show_terminal(self):
    #     self.get_terminal("sw1")
    #     self.get_terminal("sw2")
    #     self.get_terminal("ht1")
    #     self.get_terminal("ht2")
    #     self.get_log("ctl1")

    def run(self):
        logger.info("Creating Switches and Host")
        self.create_nodes()
        logger.info("Creating Ehternet Links")
        self.create_links()
        self.configure_controller()
        # self.show_terminal()


if __name__ == '__main__':
    logger = log.get_logger(__name__)

    topo = Topo()

    try:
        logger.info("Starting Network Emulation")
        logger.info("Allocating Elements Resources")
        topo.run()
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Stopping Network Emulation")
        topo.delete_all()
