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
from cnetlab.models.switches.stratum import Stratum
from cnetlab.models.servers.onos import OnosController

CONFIG = 'ONOS_APPS=gui2,drivers.bmv2,pipelines.basic,lldpprovider,hostprovider,fwd'


class Topo(Dataplane):

    def create_nodes(self):
        # Ambiete A
        self.add_node('leaf1', Stratum('leaf1'))
        self.add_node('leaf2', Stratum('leaf2'))
        self.add_node('spine1a', Stratum('spine1a'))
        self.add_node('spine2a', Stratum('spine2a'))
        self.add_node('ht1', SimpleHost('ht1'))
        self.add_node('ht2', SimpleHost('ht2'))
        
        # Ambiente B
        self.add_node('leaf1e', Stratum('leaf1e'))
        self.add_node('leaf2e', Stratum('leaf2e'))
        self.add_node('leaf1d', Stratum('leaf1d'))
        self.add_node('leaf2d', Stratum('leaf2d'))
        self.add_node('spine1b', Stratum('spine1b'))
        self.add_node('spine2b', Stratum('spine2b'))
        self.add_node('ht1e', SimpleHost('ht1e'))
        self.add_node('ht2e', SimpleHost('ht2e'))
        self.add_node('ht1d', SimpleHost('ht1d'))
        self.add_node('ht2d', SimpleHost('ht2d'))
        
        # ONOS
        self.add_node('ctl1', OnosController('ctl1', onos_app=CONFIG))

    def create_links(self):
        # Ambiente 1
        self.add_link('leaf1', 'spine1a', mtu=9000)
        self.add_link('leaf1', 'spine2a', mtu=9000)
        self.add_link('leaf2', 'spine1a', mtu=9000)
        self.add_link('leaf2', 'spine2a', mtu=9000)

        # Host Link
        ht1_src_cfg = {'ip': '10.0.0.5', 'cidr': '24', 'gw': None}
        self.add_link('ht1', 'leaf1', s_config=ht1_src_cfg, mtu=9000)
        ht2_src_cfg = {'ip': '10.0.0.6', 'cidr': '24', 'gw': None}
        self.add_link('ht2', 'leaf2', s_config=ht2_src_cfg, mtu=9000)

        # Link entre ambientes
        self.add_link('spine1a', 'spine1b')
        self.add_link('spine2a', 'spine2b')

        # Ambiente 2
        # Leaf-Leaf
        self.add_link('leaf1e', 'leaf2e', mtu=9000)
        self.add_link('leaf1d', 'leaf2d', mtu=9000)

        # Leaf-Spine lado esquerdo
        self.add_link('leaf1e', 'spine1b', mtu=9000)
        self.add_link('leaf1e', 'spine2b', mtu=9000)
        self.add_link('leaf2e', 'spine1b', mtu=9000)
        self.add_link('leaf2e', 'spine2b', mtu=9000)

        # Leaf-Spine lado direito
        self.add_link('leaf1d', 'spine1b', mtu=9000)
        self.add_link('leaf1d', 'spine2b', mtu=9000)
        self.add_link('leaf2d', 'spine1b', mtu=9000)
        self.add_link('leaf2d', 'spine2b', mtu=9000)

        # Host Link lado esquerdo
        """
        # IPs iguais nas duas interfaces
        ht1e_src_cfg = {'ip': '10.0.0.1', 'cidr': '24', 'gw': None}
        self.add_link('ht1e', 'leaf1e', s_config=ht1e_src_cfg, mtu=9000)
        self.add_link('ht1e', 'leaf2e', s_config=ht1e_src_cfg, mtu=9000)
        ht2e_src_cfg = {'ip': '10.0.0.2', 'cidr': '24', 'gw': None}
        self.add_link('ht2e', 'leaf1e', s_config=ht2e_src_cfg, mtu=9000)
        self.add_link('ht2e', 'leaf2e', s_config=ht2e_src_cfg, mtu=9000)
        """
        # IPs diferentes nas duas interfaces
        ht1e_src_cfg_l1 = {'ip': '10.0.0.1', 'cidr': '24', 'gw': None}
        self.add_link('ht1e', 'leaf1e', s_config=ht1e_src_cfg_l1, mtu=9000)
        ht1e_src_cfg_l2 = {'ip': '10.10.0.1', 'cidr': '24', 'gw': None}
        self.add_link('ht1e', 'leaf2e', s_config=ht1e_src_cfg_l2, mtu=9000)
        ht2e_src_cfg_l1 = {'ip': '10.0.0.2', 'cidr': '24', 'gw': None}
        self.add_link('ht2e', 'leaf1e', s_config=ht2e_src_cfg_l1, mtu=9000)
        ht2e_src_cfg_l2 = {'ip': '10.10.0.2', 'cidr': '24', 'gw': None}
        self.add_link('ht2e', 'leaf2e', s_config=ht2e_src_cfg_l2, mtu=9000)


        # Host Link lado direito
        """
        # IPs iguais nas duas interfaces
        ht1d_src_cfg = {'ip': '10.0.0.1', 'cidr': '24', 'gw': None}
        self.add_link('ht1d', 'leaf1d', s_config=ht1d_src_cfg, mtu=9000)
        self.add_link('ht1d', 'leaf2d', s_config=ht1d_src_cfg, mtu=9000)
        ht2d_src_cfg = {'ip': '10.0.0.2', 'cidr': '24', 'gw': None}
        self.add_link('ht2d', 'leaf1d', s_config=ht2d_src_cfg, mtu=9000)
        self.add_link('ht2d', 'leaf2d', s_config=ht2d_src_cfg, mtu=9000)
        """
        # IPs diferentes nas duas interfaces
        ht1d_src_cfg_l1 = {'ip': '10.0.0.3', 'cidr': '24', 'gw': None}
        self.add_link('ht1d', 'leaf1d', s_config=ht1d_src_cfg_l1, mtu=9000)
        ht1d_src_cfg_l2 = {'ip': '10.10.0.3', 'cidr': '24', 'gw': None}
        self.add_link('ht1d', 'leaf2d', s_config=ht1d_src_cfg_l2, mtu=9000)
        ht2d_src_cfg_l1 = {'ip': '10.0.0.4', 'cidr': '24', 'gw': None}
        self.add_link('ht2d', 'leaf1d', s_config=ht2d_src_cfg_l1, mtu=9000)
        ht2d_src_cfg_l2 = {'ip': '10.10.0.4', 'cidr': '24', 'gw': None}
        self.add_link('ht2d', 'leaf2d', s_config=ht2d_src_cfg_l2, mtu=9000)



    def show_terminal(self):
        self.get_terminal('ht1e')
        self.get_terminal('ht2e')
        self.get_terminal('ht1d')
        self.get_terminal('ht2d')
        self.get_terminal('leaf1d')
        self.get_terminal('leaf2d')
        self.get_terminal('leaf1e')
        self.get_terminal('leaf2e')
        self.get_terminal('spine1a')
        self.get_terminal('spine2a')
        self.get_terminal('spine1b')
        self.get_terminal('spine2b')
        self.get_terminal('ctl1')
        #self.get_log('spine1')
        self.get_log('ctl1')

    def set_controller(self, node, ctl):
        n = self.get_node(node)
        c = self.get_node(ctl)
        n.set_controller(c.ipctl)


    def run(self):
        self.create_nodes()
        self.create_links()
        self.show_terminal()
        self.set_controller("leaf1", 'ctl1')
        self.set_controller("leaf2", 'ctl1')
        self.set_controller("spine1a", 'ctl1')
        self.set_controller("spine2a", 'ctl1')
        self.set_controller("leaf1e",'ctl1')
        self.set_controller("leaf2e",'ctl1')
        self.set_controller("leaf1d",'ctl1')
        self.set_controller("leaf2d",'ctl1')
        self.set_controller("spine1b", 'ctl1')
        self.set_controller("spine2b", 'ctl1')
        """
        try:
            st1 = self.get_node('st1')
            ctl1 = self.get_node('ctl1')
            st1.set_ctl_pipe_basic(ctl1.ipctl)
        except Exception as ex:
            log.error(ex)
        """


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
