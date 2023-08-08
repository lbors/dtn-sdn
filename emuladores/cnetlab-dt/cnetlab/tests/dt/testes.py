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
        pass

    def get_name(self, devices, id):
        pass

    def controller(self):
        ports = {'8181/tcp': 8182,
                 '8101/tcp': 8102,
                 '5005/tcp': 5006,
                 '830/tcp': 831,
                 '9876/tcp': 9877}

        self.add_node("ctl1", OnosController("ctl1", onos_ports=ports))
        # self.add_node("ctl1", OnosController("ctl1", network='exp', onos_ports=ports))
        # self.add_node("ctl1", OnosController("ctl1"))
        self.get_log("ctl1")
        self.get_terminal("ctl1")

    def nodes(self, node):
        pass

    def hosts(self, host, node):
        pass

    def set_links(self, n_src, p_src, link_data):
        pass

    def enable_terminal(self):
        pass

    def run(self):
        # info = dt.get_infos(ip_ctl)

        logger.info("Starting Network Controller Into Dataplane")
        logger.info("Starting Onos")
        # apps = info['applications']
        self.controller()
        # time.sleep(10)

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
