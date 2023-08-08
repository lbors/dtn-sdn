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

from cnetlab.dataplane import Dataplane
from cnetlab.log import get_logger
from cnetlab.models.hosts.simplehost import SimpleHost
from cnetlab.models.servers.onos import OnosController
from cnetlab.models.switches.stratum import Stratum
from cnetlab.models.transponders.cassini import Cassini
from cnetlab.models.servers.onosconfig import SendConfigOnos

import sys

sys.path.insert(0, '/home/lucas/Documentos/UFPA/Mestrado/DT/dtsdn/')
import collector.data_request as dt


class Topology(Dataplane):
    def list_devices(self, devices):
        list_devices = []
        for device_id, device_data in devices.items():
            list_devices.append((device_data['name'], device_id))

        return list_devices

    def get_name(self, devices, id):
        try:
            return devices[id]['name']
        except Exception as ex:
            return False

    def nodes(self, devices, list_devices):
        for dev in list_devices:
            name = devices[dev[1]]['name']
            if devices[dev[1]]['sw'] == 'Stratum':
                pipeconf = devices[dev[1]]['pipeconf']
                self.add_node(name, Stratum(name, pipeconf=pipeconf))
            elif devices[dev[1]]['sw'] == 'OcNOS':
                self.add_node(name, Cassini(name))

            n = self.get_node(name)
            c = self.get_node('ctl1')
            n.set_controller(c.ipctl)

    def controller(self, apps):
        CONFIG = []
        for app in apps:
            app = app['name'].split('org.onosproject.')[1]
            CONFIG.append(app)

        APPS = "{}={}".format("ONOS_APPS", ",".join(CONFIG))
        self.add_node("ctl1", OnosController("ctl1", onos_app=APPS))
        self.get_log("ctl1")
        self.get_terminal("ctl1")

    def set_links(self, devices):
        list_links = []
        for device_id, device_data in devices.items():
            n_src = self.get_name(devices, device_id)
            links = device_data['links']

            for p_src, port_data in links.items():
                p_src = p_src.split(" ")[1]
                if not port_data['isEdgePort']:
                    n_dst = self.get_name(devices, port_data['device'])
                    p_dst = port_data['port']
                    if 'OPTICAL' in port_data['type']:
                        mode = "opt"
                        src_p = '{}-ovif{}'.format(n_src, p_src[-1:])
                        dst_p = '{}-ovif{}'.format(n_dst, p_dst[-1:])
                    else:
                        mode = "eth"
                        src_p = '{}-vif{}'.format(n_src, p_src[-1:])
                        dst_p = '{}-vif{}'.format(n_dst, p_dst[-1:])

                    if not (n_dst, n_src, dst_p, src_p, mode) in list_links:
                        list_links.append((n_src, n_dst, src_p, dst_p, mode))
                        self.add_link(n_src, n_dst, p_src=src_p, p_dst=dst_p, mode=mode)

                        c = self.get_node('ctl1')
                        s = self.get_node(n_src)
                        d = self.get_node(n_dst)
                        config.set_onos_links(c.ipctl, s, d, p_src, p_dst, link=port_data['type'])

    def enable_terminal(self):
        pass

    def run(self):
        info = dt.get_infos()
        logger.info("Starting Network Controller Into Dataplane")
        logger.info("Starting Onos")
        apps = info['applications']
        self.controller(apps)

        logger.info("Starting Nodes Into Dataplane")
        devices = info['devices']
        list_devices = self.list_devices(devices)
        self.nodes(devices, list_devices)
        logger.info("Starting Links Into Dataplane")
        self.set_links(devices)


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
