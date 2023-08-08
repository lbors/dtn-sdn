import subprocess
import sys
import os


def exec_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = p.stdout.readline()
        if output == '' or p.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").strip())


class CONFIG(object):
    def configure(self, num):
        for i in range(1, num+1):
            self.add_port_bridge_opt(i)
            self.add_port_bridge_eth(i)

    def add_port_bridge_opt(self, num):
        cmd = "ovs-vsctl add-port oe{} ovif{}".format(num, num)
        exec_cmd(cmd)
        print(cmd)

    def add_port_bridge_eth(self, num):
        cmd = "ovs-vsctl add-port xe{} vif{}".format(num, num)
        exec_cmd(cmd)
        print(cmd)


if __name__ == '__main__':
    conf = CONFIG()

    arg = sys.argv[1]
    conf.configure(int(arg))
