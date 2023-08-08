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
from cnetlab.dataplane import Dataplane
from cnetlab.log import get_logger
from cnetlab.models.hosts.simplehost import SimpleHost
from cnetlab.models.servers.onos import OnosController
from cnetlab.models.switches.stratum import Stratum

CONFIG = 'ONOS_APPS=gui2,drivers.bmv2,pipelines.fabric,lldpprovider,hostprovider,fwd'
PIPECONF_BASIC = "org.onosproject.pipelines.basic"
PIPECONF_FABRIC = "org.onosproject.pipelines.fabric"

class Topo(Dataplane):

    def create_nodes(self):
        self.add_node('leaf1', Stratum('leaf1'))
        self.add_node('leaf2', Stratum('leaf2'))
        self.add_node('spine1', Stratum('spine1'))
        self.add_node('spine2', Stratum('spine2'))
        self.add_node('ht1', SimpleHost('ht1'))
        self.add_node('ht2', SimpleHost('ht2'))
        self.add_node('ctl1', OnosController('ctl1', onos_app=CONFIG))

    def create_links(self):
        self.add_link('leaf1', 'spine1', mtu=9000)
        self.add_link('leaf1', 'spine2', mtu=9000)
        self.add_link('leaf2', 'spine1', mtu=9000)
        self.add_link('leaf2', 'spine2', mtu=9000)

        # Host Link
        ht1_src_cfg = {'ip': '10.0.0.1', 'cidr': '24', 'gw': None}
        self.add_link('ht1', 'leaf1', s_config=ht1_src_cfg, mtu=9000)
        ht2_src_cfg = {'ip': '10.0.0.2', 'cidr': '24', 'gw': None}
        self.add_link('ht2', 'leaf2', s_config=ht2_src_cfg, mtu=9000)

    def show_terminal(self):
        self.get_terminal('ht1')
        self.get_terminal('ht2')
        self.get_terminal('leaf1')
        self.get_terminal('leaf2')
        self.get_terminal('spine1')
        self.get_terminal('spine2')
        self.get_terminal('ctl1')
        self.get_log('spine1')
        self.get_log('ctl1')

    def set_controller(self, node, ctl):
        mods = [
            "org.onosproject.drivers.stratum",
            "org.onosproject.pipelines.fabric",
            "org.onosproject.drivers.gnmi",
            "org.onosproject.protocols.grpc",
            "org.onosproject.generaldeviceprovider",
            "org.onosproject.drivers.odtn-driver",
            "org.onosproject.drivers.p4runtime",
            "org.onosproject.pipelines.basic",
            "org.onosproject.drivers.gnoi",
            "org.onosproject.drivers.bmv2"
        ]
        n = self.get_node(node)
        c = self.get_node(ctl)
        n.set_controller(c.ipctl, mods)

    def run(self):
        self.create_nodes()
        self.create_links()
        self.show_terminal()
        self.set_controller("leaf1", 'ctl1')
        self.set_controller("leaf2", 'ctl1')
        self.set_controller("spine1", 'ctl1')
        self.set_controller("spine2", 'ctl1')


if __name__ == '__main__':
    log = get_logger(__name__)

    dp = Topo()

    try:
        dp.run()
        while True:
            pass
    except KeyboardInterrupt:
        log.info("finishing the network emulation")
        dp.delete_all()
