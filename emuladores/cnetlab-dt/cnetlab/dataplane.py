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

import logging

from cnetlab.iproute import IPR

logger = logging.getLogger(__name__)


class NodeFabric(object):
    def __init__(self):
        self._nodes = {}

    def get_nodes(self, data=False):
        ret = []
        if data:
            for k, v in self._nodes.items():
                ret.append((k, v))
                return ret.copy()
        else:
            ret += self._nodes.keys()
            return ret.copy()

    def add_node(self, name, **att):
        data = {}
        for k, v in att.items():
            data.update({k: v})
        self._nodes.update({name: data})

    def get_node(self, name):
        return self._nodes.get(name, None)

    def del_node(self, name):
        del (self._nodes[name])

    def has_node(self, name):
        if name in self._nodes.keys():
            return True
        else:
            return False


class LinkFabric(object):
    def __init__(self):
        self._links = {}

    def get_links(self, data=False):
        ret = []
        if data:
            for k, v in self._links.items():
                ret.append((k[0], k[1], v))
                return ret.copy()
        else:
            ret += self._links.keys()
            return ret.copy()

    def add_link(self, src, dst, **att):
        data = {}
        for k, v in att.items():
            data.update({k: v})
        self._links.update({(src, dst): data})

    def get_link(self, src, dst):
        key = (src, dst)
        return self._links.get(key, None)

    def del_link(self, src, dst):
        key = (src, dst)
        del (self._links[key])

    def has_link(self, src, dst):
        key = (src, dst)
        if key in self._links.keys():
            return True
        else:
            return False


class Dataplane(object):

    def __init__(self):
        self._nodes = NodeFabric()
        self._links = LinkFabric()

    def get_nodes(self, data=False):
        return self._nodes.get_nodes(data)

    def get_links(self, data=False):
        return self._links.get_links(data)

    def add_node(self, name, node):
        try:
            node.commit()
            self._nodes.add_node(name, node=node)
        except Exception as ex:
            logger.error(ex)

    def del_node(self, name):
        try:
            node = self.get_node(name)
            node.delete()
            self._nodes.del_node(name)
        except Exception as ex:
            logger.error(ex)

    def get_node(self, name):
        return self._nodes.get_node(name)['node']

    def has_node(self, name):
        return self._nodes.has_node(name)

    def add_link(self, src, dst, **params):
        # TODO: Choose another way to implement this
        src_cfg = params.get("src_cfg", None)
        dst_cfg = params.get("dst_cfg", None)

        p_src = params.get("p_src", None)
        p_dst = params.get("p_dst", None)
        try:
            n_src = self.get_node(src)
            n_dst = self.get_node(dst)

            if p_src is None:
                p_src = n_src.get_port(**params)
                # p_dst = n_dst.get_port(**params)
            if p_dst is None:
                p_dst = n_dst.get_port(**params)

            IPR(netns=None).set_veth(p_src, p_dst)
            n_src.add_port(name=p_src, config=src_cfg, **params)
            n_dst.add_port(name=p_dst, config=dst_cfg, **params)
            self._links.add_link(src, dst, ports=(p_src, p_dst), **params)
            logger.info("new link between {}--{} has created".format(src, dst))
        except Exception as ex:
            logger.error(ex)

    def del_link(self, src, dst, **params):
        # TODO: Choose another way to implement this
        assert self.has_link(src, dst), "The link between {}-{} not exist".format(src, dst)
        try:
            link = self.get_link(src, dst)
            n_src = self.get_node(src)
            n_dst = self.get_node(dst)
            n_src.rem_port(name=link["ports"][0], **params)
            n_dst.rem_port(name=link["ports"][1], **params)
            self._links.del_link(src, dst)
            logger.info("the link between {}--{} was deleted".format(src, dst))
        except Exception as ex:
            logger.error(ex)

    def get_link(self, src, dst):
        return self._links.get_link(src, dst)

    def has_link(self, src, dst):
        return self._links.has_link(src,dst)

    def get_terminal(self, name):
        try:
            node = self.get_node(name)
            node.terminal(type="cli")
        except Exception as ex:
            logger.error(ex)

    def get_log(self, name):
        try:
            node = self.get_node(name)
            node.terminal(type="logs")
        except Exception as ex:
            logger.error(ex)

    def delete_all(self, **params):
        links = self.get_links()
        if len(links) > 0:
            for l in links:
                self.del_link(l[0], l[1], **params)
        else:
            logger.warning("there are not links to delete")

        nodes = self.get_nodes()
        if len(nodes) > 0:
            for n in nodes:
                self.del_node(n)
        else:
            logger.warning("there are not nodes to delete")
