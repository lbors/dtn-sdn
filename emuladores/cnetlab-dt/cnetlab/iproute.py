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

from pyroute2 import IPRoute, NetNS
import logging

logger = logging.getLogger(__name__)


def ipr_add_veth(ifname, ifpeer, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    ipr.link('add', ifname=ifname, peer=ifpeer, kind='veth')
    ipr.close()


def ipr_add_bridge(ifname, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    ipr.link('add', ifname=ifname, kind='bridge')
    ipr.close()


def ipr_add_if_br(br, ifname, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    idx_br = ipr.link_lookup(ifname=br)[0]
    idx_ifname = ipr.link_lookup(ifname=ifname)[0]
    ipr.link("set", index=idx_ifname, master=idx_br)
    ipr.close()


def ipr_rem_if_br(ifname, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    idx_ifname = ipr.link_lookup(ifname=ifname)[0]
    ipr.link("set", index=idx_ifname, master=None)
    ipr.close()


def ipr_if_up(ifname, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    idx_ifname = ipr.link_lookup(ifname=ifname)[0]
    ipr.link('set', index=idx_ifname, state='up')
    ipr.close()


def ipr_if_down(ifname, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    idx_ifname = ipr.link_lookup(ifname=ifname)[0]
    ipr.link('set', index=idx_ifname, state='down')
    ipr.close()


def ipr_if_del(ifname, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    ipr.link('del', ifname=ifname)
    ipr.close()


def ipr_if_config(ifname, address, cidr, gw, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    if address is None:
        ipr.close()
        raise RuntimeError("the ip addresses cannot be null")
    idx_ifname = ipr.link_lookup(ifname=ifname)[0]
    ipr.addr('add', index=idx_ifname, address=address, mask=int(cidr))
    if gw is not None:
        ipr.route('add', dst='default', gateway=gw)
    ipr.close()


def ipr_set_mtu(ifname, mtu, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    idx_ifname = ipr.link_lookup(ifname=ifname)[0]
    ipr.link('set', index=idx_ifname, mtu=int(mtu))
    ipr.close()


def ipr_set_name(ifname, name, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    idx_ifname = ipr.link_lookup(ifname=ifname)[0]
    ipr.link('set', index=idx_ifname, name=name)
    ipr.close()


def ipr_add_if_ns(ifname, netns):
    ipr = IPRoute()
    idx_ifname = ipr.link_lookup(ifname=ifname)[0]
    ipr.link('set', index=idx_ifname, net_ns_fd=netns)
    ipr.close()


def ipr_has_if(ifname, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    idx = ipr.link_lookup(ifname=ifname)
    if len(idx) > 0:
        ipr.close()
        return True

    else:
        ipr.close()
        return False

def ipr_set_mac(ifname, mac, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    ipr.link("set", index=ipr.link_lookup(ifname=ifname)[0], address=mac)
    ipr.close()

def ipr_set_if_vlan(ifname, vlanid, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    ipr.link("add", ifname="vlan{}".format(vlanid),
             link=ipr.link_lookup(ifname=ifname)[0],
             kind="vlan", vlan_id=vlanid)
    ipr.close()
    return 'vlan{}'.format(vlanid)

def ipr_set_route(dst, gw, netns):
    ipr = (IPRoute() if netns is None else NetNS(netns=netns))
    ipr.route("add",
              dst=dst,
              gateway=gw
    )
    ipr.close()

class IPR(object):

    def __init__(self, netns):
        self._netns = netns

    def set_if_ns(self, ifname):
        try:
            ipr_add_if_ns(ifname, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_up(self, ifname):
        try:
            ipr_if_up(ifname, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_down(self, ifname):
        try:
            ipr_if_down(ifname, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_del(self, ifname):
        try:
            ipr_if_del(ifname, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_veth(self, ifname, ifpeer):
        try:
            ipr_add_veth(ifname, ifpeer, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_mtu(self, ifname, mtu):
        try:
            ipr_set_mtu(ifname, mtu, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_name(self, ifname, new_name):
        try:
            ipr_if_down(ifname, netns=self._netns)
            ipr_set_name(ifname, new_name, netns=self._netns)
            ipr_if_up(new_name, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_bridge(self, ifname):
        try:
            ipr_add_bridge(ifname, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_if_bridge(self, bridge, ifname):
        try:
            ipr_add_if_br(bridge, ifname, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def rem_if_bridge(self, ifname):
        try:
            ipr_rem_if_br(ifname, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_address(self, ifname, address, cidr, gw=None):
        try:
            ipr_if_config(ifname, address, cidr, gw, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def has_if(self, ifname):
        try:
            return ipr_has_if(ifname, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_if_vlan(self, ifname, vlanid):
        try:
            return ipr_set_if_vlan(ifname, vlanid, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_mac(self, ifname, mac):
        try:
            ipr_set_mac(ifname, mac, netns=self._netns)
        except Exception as ex:
            logger.error(ex)

    def set_route(self, dst, gateway):
        try:
            ipr_set_route(dst, gateway,netns=self._netns)
        except Exception as ex:
            logger.error(ex)