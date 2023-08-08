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
from pathlib import Path
import subprocess
import logging
import os
import docker
import itertools
from cnetlab.iproute import IPR

logger = logging.getLogger(__name__)


class Node(object):
    def __init__(self, name, image, url="localhost", **params):
        self.name = name
        self.image = image
        self.client = url
        self.container = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = '{}'.format(value)

    @property
    def client(self):
        return self.__client

    @client.setter
    def client(self, v):
        if v.__eq__("localhost"):
            self.__client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        else:
            self.__client = docker.DockerClient(base_url=v)

    @property
    def pid(self):
        return self.container.attrs["State"]["Pid"]

    @property
    def ipctl(self):
        return self.container.attrs["NetworkSettings"]["IPAddress"]

    @property
    def status(self):
        return self.container.attrs["State"]["Status"]

    def init(self):
        conf = dict()
        conf.update(
            detach=True,
            cap_add=["ALL", "NET_ADMIN"],
            privileged=True,
            tty=True,
            name=self.name,
            hostname=self.name,
            environment=["container=Docker"],
        )
        return conf.copy()

    def start(self, **params):
        self.client.containers.run(self.image, **params)
        self.container = self.client.containers.get(self.name)
        os.makedirs("/var/run/netns", exist_ok=True)
        os.symlink("/proc/{pid}/ns/net".format(pid=self.pid), "/var/run/netns/{name}".format(name=self.name))

    def stop(self):
        self.container.remove(force=True)
        os.remove("/var/run/netns/{name}".format(name=self.name))

    def exec_cmd(self, cmd):
        return self.container.exec_run(cmd=cmd, tty=True, privileged=True)

    def terminal(self, type='cli'):
        terminal = Path('/usr/bin/xterm')
        dcr = Path('/usr/bin/docker')

        def do_terminal():
            return ["{cmd} -T {node_name} -fg white -bg black -fa "
                    "'Liberation Mono' -fs 10 -e {d_cmd} exec -it "
                    "{node_name} {shell}".format(cmd=terminal.as_posix(),
                                                 d_cmd=dcr.as_posix(),
                                                 node_name=self.name,
                                                 shell='bash')]

        def do_logs():
            return ["{cmd} -T {node_name} -fg white -bg black -fa "
                    "'Liberation Mono' -fs 10 -e {d_cmd} logs -f "
                    "{node_name}".format(cmd=terminal.as_posix(), d_cmd=dcr.as_posix(), node_name=self.name)]

        if terminal.is_file():
            if type.__eq__('cli'):
                cmd = do_terminal()
            elif type.__eq__('logs'):
                cmd = do_logs()
            else:
                raise RuntimeError("type terminal not found")

            subprocess.Popen(cmd, shell=True)
        else:
            raise RuntimeError("xterm is not found")

    def get_port(self, **params):
        pass

    def commit(self):
        pass

    def delete(self):
        pass

    def add_port(self, **params):
        pass

    def rem_port(self, **params):
        pass
