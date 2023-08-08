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
        self.add_node("df", Whitebox("df"))
        self.add_node("to", Whitebox("to"))
        self.add_node("pa", Whitebox("pa"))
        self.add_node("ma", Whitebox("ma"))
        self.add_node("pi", Whitebox("pi"))
        self.add_node("ce", Whitebox("ce"))
        
        self.add_node("df-ht", SimpleHost("df-ht"))
        self.add_node("to-ht", SimpleHost("to-ht"))
        self.add_node("pa-ht", SimpleHost("pa-ht"))
        self.add_node("ma-ht", SimpleHost("ma-ht"))
        self.add_node("pi-ht", SimpleHost("pi-ht"))
        self.add_node("ce-ht", SimpleHost("ce-ht"))

        self.add_node("ctl1", OnosController("ctl1"))

    def create_links(self):
        self.add_link(src="df", dst="to")
        self.add_link(src="df", dst="ma")
        self.add_link(src="df", dst="ce")
        self.add_link(src="to", dst="pa")
        self.add_link(src="pa", dst="ma")
        self.add_link(src="ma", dst="pi")
        self.add_link(src="pi", dst="ce")

        
        self.add_link(src="df-ht", dst="df", src_cfg={'ip': '10.0.2.1', 'cidr': '24', 'gw': "10.0.2.254"})
        self.add_link(src="to-ht", dst="to", src_cfg={'ip': '10.0.3.1', 'cidr': '24', 'gw': "10.0.3.254"})
        self.add_link(src="pa-ht", dst="pa", src_cfg={'ip': '10.0.4.1', 'cidr': '24', 'gw': "10.0.4.254"})
        self.add_link(src="ma-ht", dst="ma", src_cfg={'ip': '10.0.5.1', 'cidr': '24', 'gw': "10.0.5.254"})
        self.add_link(src="pi-ht", dst="pi", src_cfg={'ip': '10.0.6.1', 'cidr': '24', 'gw': "10.0.6.254"})
        self.add_link(src="ce-ht", dst="ce", src_cfg={'ip': '10.0.7.1', 'cidr': '24', 'gw': "10.0.7.254"})
        

    def configure_controller(self):
        ctl1 = self.get_node("ctl1")
        df = self.get_node("df")
        df.set_controller(ctl1.ipctl, 6653)
        to = self.get_node("to")
        to.set_controller(ctl1.ipctl, 6653)
        pa = self.get_node("pa")
        pa.set_controller(ctl1.ipctl, 6653)
        ma = self.get_node("ma")
        ma.set_controller(ctl1.ipctl, 6653)
        pi = self.get_node("pi")
        pi.set_controller(ctl1.ipctl, 6653)
        ce = self.get_node("ce")
        ce.set_controller(ctl1.ipctl, 6653)

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
