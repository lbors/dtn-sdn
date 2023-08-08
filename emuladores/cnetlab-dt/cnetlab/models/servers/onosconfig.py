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

import json
import logging
import socket
import threading
import time

from requests import Session

from cnetlab.dataplane import Dataplane

logger = logging.getLogger(__name__)


def get_status_app(ip_ctl, mod):
    with Session() as s:
        try:
            url = "http://{}:8181/onos/v1/applications/{}".format(ip_ctl, mod)
            auth = ('karaf', 'karaf')
            s.headers.update({"Accept": "application/json"})
            ret = s.get(url=url, auth=auth)
            if ret.ok:
                return True
            else:
                return False
        except Exception as ex:
            return False


def link_config(src_id, src_port, dst_id, dst_port, link_type):
    config = {
        'links': {
            '{}/{}-{}/{}'.format(src_id, src_port, dst_id, dst_port): {
                'basic': {
                    'type': '{}'.format(link_type),
                    'metric': 1,
                    'durable': True,
                    'bidirectional': True
                }
            }
        }
    }
    return config.copy()


def stratum_config_link_host(src_id, src_port, dst, gw, cidr, vlan_id, t_vlan):
    if t_vlan == "untagged":
        config = {
            'ports': {
                '{}/{}'.format(src_id, src_port): {
                    'interfaces': [
                        {
                            'name': '{}'.format(dst.name),
                            'ips': [
                                '{}/{}'.format(gw, cidr)
                            ],
                            'vlan-{}'.format(t_vlan): vlan_id
                        }
                    ]
                }
            }
        }
    else:
        config = {
            'ports': {
                '{}/{}'.format(src_id, src_port): {
                    'interfaces': [
                        {
                            'name': '{}'.format(dst.name),
                            'ips': [
                                '{}/{}'.format(gw, cidr)
                            ],
                            'vlan-{}'.format(t_vlan): [vlan_id]
                        }
                    ]
                }
            }
        }

    return config.copy()


class SendConfigOnos(Dataplane):
    def send_ctl_config(self, ip_ctl, json):

        with Session() as s:
            url = "http://{}:8181/onos/v1/network/configuration/".format(ip_ctl)
            auth = ('karaf', 'karaf')
            s.headers.update({"Content-Type": "application/json"})
            ret = s.post(url=url, auth=auth, data=json)
            if ret.ok:
                # TODO
                # logger.info(" {} was connected to onos".format(src))
                return True
            else:
                logger.info(ret.content)
                return False

    def modules_is_running(self, ip_ctl, mods):
        run = True
        while run:
            for m in mods:
                if get_status_app(ip_ctl, m):
                    mods.remove(m)
                    logger.debug("the module ({}) is running".format(m))
                if len(mods) == 0:
                    run = False
                    logger.debug("all modules is running")
                time.sleep(2)
        return True

    def send_link_config(self, src, dst, ip_ctl, mods, j):
        exit = False
        logger.info("waiting nodes to configure links")
        while not exit:
            if src.connected and dst.connected:
                time.sleep(10)
                logger.info(j)
                self.modules_is_running(ip_ctl, mods)
                self.send_ctl_config(ip_ctl, j)
                exit = True

        # logger.info("onos links was configured")
        logger.info("onos links between {}--{} was configured".format(src.name, dst.name))

    def set_onos_links(self, ctl, src, dst, src_port, dst_port, **params):
        link_type = params.get('link', 'DIRECT')

        mods = [
            'org.onosproject.lldpprovider',
            'org.onosproject.netcfglinksprovider',
            'org.onosproject.segmentrouting',
            'org.onosproject.proxyarp'
        ]

        # c = self.get_node(ctl)
        # s = self.get_node(src)
        # d = self.get_node(dst)

        sid = src.onos_id
        did = dst.onos_id

        cfg = link_config(sid, src_port, did, dst_port, link_type)

        j = json.dumps(cfg, indent=2)

        links = threading.Thread(target=self.send_link_config, args=(src, dst, ctl, mods, j))
        links.start()

    def set_stratum_host(self, ctl, src, host, src_port, gw, cidr, vlan_id, **params):
        t_vlan = params.get('vlan', 'untagged')

        mods = [
            'org.onosproject.lldpprovider'
        ]

        # s = self.get_node(src)
        # d = self.get_node(dst)
        # c = self.get_node(ctl)

        sid = src.onos_id

        cfg = stratum_config_link_host(sid, src_port, host, gw, cidr, vlan_id, t_vlan)

        j = json.dumps(cfg, indent=2)

        links = threading.Thread(target=self.send_link_config, args=(src, host, ctl, mods, j))
        links.start()
