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
        self.add_node('st1', Stratum('st1', pipeconf=PIPECONF_FABRIC))
        self.add_node('st2', Stratum('st2', pipeconf=PIPECONF_FABRIC))
        self.add_node('ht1', SimpleHost('ht1'))
        self.add_node('ht2', SimpleHost('ht2'))
        self.add_node('ctl1', OnosController('ctl1', onos_app=CONFIG))

    def create_links(self):
        self.add_link('st1', 'st2')
        ht1_src_cfg = {'ip': '10.0.0.1', 'cidr': '24', 'vlan': 10}
        self.add_link('ht1', 'st1', src_cfg=ht1_src_cfg)
        ht2_src_cfg = {'ip': '10.0.0.2', 'cidr': '24', 'vlan': 10}
        self.add_link('ht2', 'st2', src_cfg=ht2_src_cfg)

    def show_terminal(self):
        self.get_terminal('st1')
        self.get_terminal('st2')
        self.get_terminal('ht1')
        self.get_terminal('ht2')
        self.get_terminal('ctl1')
        self.get_log('st1')
        self.get_log('ctl1')

    def set_controller(self, node, ctl):
        n = self.get_node(node)
        c = self.get_node(ctl)
        n.set_controller(c.ipctl)

    def run(self):
        self.create_nodes()
        self.create_links()
        self.show_terminal()
        self.set_controller('st1', 'ctl1')
        self.set_controller('st2', 'ctl1')


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
