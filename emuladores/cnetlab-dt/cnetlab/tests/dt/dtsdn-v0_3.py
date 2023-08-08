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
import json

ip_ctl = "172.19.0.2"


class Topology(Dataplane):
    def name_devices(self, devices):
        list_devices = []
        for device_id, device_data in devices.items():
            list_devices.append((device_data['name'], device_id))

        return list_devices

    def get_name(self, devices, id):
        try:
            return devices[id]['name']
        except Exception as ex:
            return False

    def controller(self, apps):
        if self.has_node("ctl1"):
            logger.info("Onos já está iniciado")
            pass
        else:
            logger.info("Starting Network Controller Into Dataplane")
            logger.info("Starting Onos")

            CONFIG = []
            for app in apps:
                app = app['name'].split('org.onosproject.')[1]
                CONFIG.append(app)

            APPS = "{}={}".format("ONOS_APPS", ",".join(CONFIG))
            self.add_node("ctl1", OnosController("ctl1", onos_app=APPS))
            # self.get_log("ctl1")
            # self.get_terminal("ctl1")

    def nodes(self, devices):
        for dev_id, dev_data in devices.items():
            name = dev_data['name']
            sw = dev_data['sw']
            if self.has_node(name):
                if dev_data['available']:
                    logger.info("Node {} Into Dataplane".format(name))
                    pass
                else:
                    logger.info("Stopping Nodes {} Into Dataplane".format(name))
                    self.del_node(dev_data['name'])

            else:
                logger.info("Starting Node {} Into Dataplane".format(name))
                c = self.get_node('ctl1')
                if 'Stratum' in sw:
                    pipeconf = dev_data['pipeconf']
                    sid = dev_data['sid']
                    mac = dev_data['mac']
                    self.add_node(name, Stratum(name, pipeconf=pipeconf))
                    n = self.get_node(name)
                    n.set_controller(c.ipctl, sid=sid, mac=mac, edge=dev_data['isEdgeRouter'])

                elif 'OcNOS' in sw:
                    self.add_node(name, Cassini(name))
                    n = self.get_node(name)
                    n.set_controller(c.ipctl)
                else:
                    pass

    def hosts(self, hosts):
        host_cfg = {}

        for host_id, host_data in hosts.items():
            host_name = host_data["name"]
            if self.has_node(host_name):
                pass
            else:
                logger.info("Starting Host {} Into Dataplane".format(host_name))
                self.add_node(host_name, SimpleHost(host_name, ctl=False))

                n_src = host_name
                src_p = '{}-vif{}'.format(n_src, "1")
                n_dst = host_data['device'].split(':')[1]
                dst_p = '{}-vif{}'.format(n_dst, host_data['port'])

                host_cfg.update({'ip': "{}".format(host_data['ip']),
                                 'cidr': "{}".format(host_data['cidr']),
                                 'gw': "{}".format(host_data['gw'])})

                self.add_link(n_src, n_dst, p_src=src_p, p_dst=dst_p, src_cfg=host_cfg)

                c = self.get_node('ctl1')
                h = self.get_node(n_src)
                d = self.get_node(n_dst)
                config.set_stratum_host(c.ipctl, d, h,
                                        host_data['port'],
                                        host_data['gw'],
                                        host_data['cidr'],
                                        host_data['vlan_number'])

    def set_links(self, devices):
        # print(json.dumps(devices, indent=2))

        for dev_id, dev_data in devices.items():
            n_src = dev_data['name']
            links = dev_data['links']
            for port_data, link_data in links.items():
                n_dst = link_data['device']
                # p_src = port_data.split(" ")[1]
                # p_dst = link_data['port']

                if self.has_link(n_src, n_dst) or self.has_link(n_dst, n_src) and not link_data['isEdgePort']:
                    if 'ACTIVE' in link_data['state']:
                        logger.info("Link between {} - {} Into Dataplane".format(n_src, n_dst))
                        pass
                    else:
                        pass
                        logger.info("Stopping Link between {} - {} Into Dataplane".format(n_src, n_dst))
                        self.del_link(n_src, n_dst)
                        self.del_node(dev_data['name'])

                else:
                    logger.info("Starting Links between {} and {} Into Dataplane".format(n_src, n_dst))
                    p_src = port_data.split(" ")[1]

                    if link_data['isEdgePort']:
                        # mode = "eth"
                        # src_p = '{}-vif{}'.format(n_src, p_src[-1:])
                        #TODO
                        #Verificar o modo de identificação das portas
                        # self.add_link(n_src, n_dst, p_src=src_p, mode=mode)
                        pass

                    else:
                        p_dst = link_data['port']
                        if 'OPTICAL' in link_data['type']:
                            mode = "opt"
                            src_p = '{}-ovif{}'.format(n_src, p_src[-1:])
                            dst_p = '{}-ovif{}'.format(n_dst, p_dst[-1:])
                        else:
                            mode = "eth"
                            src_p = '{}-vif{}'.format(n_src, p_src[-1:])
                            dst_p = '{}-vif{}'.format(n_dst, p_dst[-1:])

                        self.add_link(n_src, n_dst, p_src=src_p, p_dst=dst_p, mode=mode)

                        c = self.get_node('ctl1')
                        s = self.get_node(n_src)
                        d = self.get_node(n_dst)

                        config.set_onos_links(c.ipctl, s, d, p_src, p_dst, link=link_data['type'])


    def enable_terminal(self):
        pass

    def run(self):
        info = dt.get_infos(ip_ctl)

        logger.info("Checking Onos")
        apps = info['applications']
        self.controller(apps)

        logger.info("Checking Nodes Into Dataplane")
        devices = info['devices']
        self.nodes(devices)

        logger.info("Checking Links Into Dataplane")
        self.set_links(devices)

        logger.info("Checking Hosts Into Dataplane")
        if info['hosts'] != {}:
            self.hosts(info['hosts'])


if __name__ == '__main__':
    logger = get_logger(__name__)
    config = SendConfigOnos()
    dev_control = {}
    list_links = []

    dp = Topology()

    try:
        dp.run()
        while True:
            logger.info("Wait 60s to run again")
            time.sleep(60)
            logger.info("Check components")
            dp.run()
            pass
    except KeyboardInterrupt:
        logger.info("Stopping network emulation")
        dp.delete_all()
