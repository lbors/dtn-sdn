# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright  (c) 2020  National Network for Education and Research (RNP)      +
#                                                                              +
#  Licensed under the Apache License, Version 2.0 (the "License");             +
#  you may not use this file except in compliance with the License.            +
#  You may obtain a copy of the License at                                     +
#                                                                              +
#      http://www.apache.org/licenses/LICENSE-2.0                              +
#                                                                              +
#  Unless required by applicable law or agreed to in writing, software         +
#  distributed under the License is distributed on an "AS IS" BASIS,           +
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    +
#  See the License for the specific language governing permissions and         +
#  limitations under the License.                                              +
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import subprocess
import os
import time

def exec_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = p.stdout.readline()
        if output == '' or p.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").strip())

def ports():
    interfaces = os.listdir('/sys/class/net/')

    eth = 0
    
    for i in interfaces:
        if i[:-1] == 'vif':
            eth += 1

    add_port(eth)


def add_port(eth):

    for i in range(1, eth+1):
        cmd = "ovs-vsctl add-port br0 vif{}".format(i)
        exec_cmd(cmd)
        time.sleep(1)
        

def create_bridge():
    name = "br0"
    try:
        cmd = "ovs-vsctl add-br {}".format(name)
        exec_cmd(cmd)

    except Exception as ex:
        # logger.error(ex)
        pass

def delete_bridge(self, name):
    
    try:
        cmd = "ovs-vsctl add-br {}".format(name)
        exec_cmd(cmd)
        
    except Exception as ex:
        # self.logger.error(ex)
        pass

def init():
    create_bridge()
    try:
        ports()
        # logger.warning("Application exit requested, exiting.\n")
    finally:
        pass
    #     delete_bridge(bridge_name)

if __name__ == '__main__':
    init()
