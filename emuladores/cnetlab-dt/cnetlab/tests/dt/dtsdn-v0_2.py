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
import time

from cnetlab.dataplane import Dataplane
from cnetlab.log import get_logger
from cnetlab.models.hosts.simplehost import SimpleHost
from cnetlab.models.servers.onos import OnosController
from cnetlab.models.switches.stratum import Stratum
from cnetlab.models.transponders.cassini import Cassini
from cnetlab.models.servers.onosconfig import SendConfigOnos
from cnetlab.models.dtsdn.collector import data_request as dt

ip_ctl = "172.19.0.2"


class Topology(Dataplane):
    def name_devices(self, devices):
        list_devices = []
        for device_id, device_data in devices.items():
            list_devices.append((device_data['name'], device_id))

        # print(list_devices)

        return list_devices

    def get_name(self, devices, id):
        try:
            return devices[id]['name']
        except Exception as ex:
            return False

    def controller(self, apps):
        CONFIG = []
        for app in apps:
            app = app['name'].split('org.onosproject.')[1]
            CONFIG.append(app)

        APPS = "{}={}".format("ONOS_APPS", ",".join(CONFIG))
        self.add_node("ctl1", OnosController("ctl1", onos_app=APPS))
        self.get_log("ctl1")
        self.get_terminal("ctl1")

    def nodes(self, node):
        name = node['name']
        if 'Stratum' in node['sw']:
            pipeconf = node['pipeconf']
            self.add_node(name, Stratum(name, pipeconf=pipeconf))
        elif 'OcNOS' in node['sw']:
            self.add_node(name, Cassini(name))
        else:
            pass

        n = self.get_node(name)
        c = self.get_node('ctl1')
        n.set_controller(c.ipctl)

    def hosts(self, host, node):
        host_cfg = {}
        self.add_node(host, SimpleHost(host, ctl=False))
        n_src = host
        n_dst = node['device'].split(':')[1]
        dst_p = '{}-vif{}'.format(n_dst, node['port'])
        src_p = host.split('ht')[1]
        src_p = '{}-vif{}'.format(n_src, src_p)

        host_cfg.update({'ip': "{}".format(node['ip']),
                         'cidr': "{}".format(node['cidr']),
                         'gw': "{}".format(node['gw'])})

        self.add_link(n_src, n_dst, p_src=src_p, p_dst=dst_p, src_cfg=host_cfg)

        c = self.get_node('ctl1')
        s = self.get_node(n_dst)
        h = self.get_node(n_src)
        config.set_stratum_host(c.ipctl, s, h, node['port'], node['gw'], node['cidr'],
                                node['vlan'])

    def set_links(self, n_src, p_src, link_data):
        if not link_data['isEdgePort']:
            n_dst = dev_control[link_data['device']]['name']
            p_dst = link_data['port']

            if 'OPTICAL' in link_data['type']:
                mode = "opt"
                src_p = '{}-ovif{}'.format(n_src, p_src[-1:])
                dst_p = '{}-ovif{}'.format(n_dst, p_dst[-1:])
            else:
                mode = "eth"
                src_p = '{}-vif{}'.format(n_src, p_src[-1:])
                dst_p = '{}-vif{}'.format(n_dst, p_dst[-1:])

            if n_src and n_dst not in dev_control:
                dev_control.update({n_src: {src_p: 'ACTIVE'},
                                    n_dst: {dst_p: 'ACTIVE'}})
                self.add_link(n_src, n_dst, p_src=src_p, p_dst=dst_p, mode=mode)
                c = self.get_node('ctl1')
                s = self.get_node(n_src)
                d = self.get_node(n_dst)
                config.set_onos_links(c.ipctl, s, d, p_src, p_dst, link=link_data['type'])
            else:
                if src_p in dev_control[n_src] or dst_p in dev_control[n_dst]:
                    pass
                else:
                    dev_control[n_src].update({src_p: 'ACTIVE'})
                    dev_control[n_dst].update({dst_p: 'ACTIVE'})
                    self.add_link(n_src, n_dst, p_src=src_p, p_dst=dst_p, mode=mode)
                    # c = self.get_node('ctl1')
                    # s = self.get_node(n_src)
                    # d = self.get_node(n_dst)
                    # config.set_onos_links(c.ipctl, s, d, p_src, p_dst, link=link_data['type'])
        else:
            # mode = "eth"
            # src_p = '{}-vif{}'.format(n_src, p_src[-1:])
            # self.nodes()
            # self.add_link(n_src, n_dst, p_src=src_p, mode=mode)

            pass

    def enable_terminal(self):
        pass

    def run(self):
        # info = dt.get_infos(ip_ctl)

        logger.info("Starting Network Controller Into Dataplane")
        logger.info("Starting Onos")
        # apps = info['applications']
        # self.controller(apps)
        self.add_node("ctl1", OnosController("ctl1", network='teste'))
        time.sleep(10)
        #
        # logger.info("Starting Nodes Into Dataplane")
        # devices = info['devices']
        # for dev_id, dev_data in devices.items():
        #     if dev_id not in dev_control:
        #         self.nodes(dev_data)
        #         dev_control.update({dev_id: {
        #             'name': dev_data['name'],
        #             'available': dev_data['available'],
        #         }})
        #     else:
        #         if dev_data['available'] == dev_control[dev_id]['available']:
        #             pass
        #         else:
        #             logger.info("Stopping Nodes Into Dataplane")
        #             self.del_node(dev_data['name'])
        #             dev_control.pop(dev_id)
        #
        # logger.info("Starting Links Into Dataplane")
        # for dev_id, dev_data in devices.items():
        #     n_src = dev_data['name']
        #     links = dev_data['links']
        #     for p_src, link_data in links.items():
        #         p_src = p_src.split(" ")[1]
        #         self.set_links(n_src, p_src, link_data)
        #
        # logger.info("Starting Hosts Into Dataplane")
        # hosts = info['hosts']
        # for host, host_data in hosts.items():
        #     self.hosts(host, host_data)
        #
        #     pass


if __name__ == '__main__':
    logger = get_logger(__name__)
    config = SendConfigOnos()
    dev_control = {}
    list_links = []

    dp = Topology()

    try:
        dp.run()
        while True:
            # dp.run()
            pass
    except KeyboardInterrupt:
        logger.info("Stopping network emulation")
        dp.delete_all()
