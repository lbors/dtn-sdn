import subprocess
import sys
import yaml


def exec_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = p.stdout.readline()
        if output == '' or p.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").strip())


class OVS(object):
    def add_port_bridge(self, list):
        bridge, port = list[0], list[1]
        cmd = "ovs-vsctl add-port {} {}".format(bridge, port)
        exec_cmd(cmd)
        print(cmd)

    def rem_port_bridge(self, bridge, port):
        cmd = "ovs-vsctl del-port {} {}".format(bridge, port)
        exec_cmd(cmd)
        print(cmd)

    def add_bridge(self, name):
        cmd = "ovs-vsctl add-br {}".format(name)
        exec_cmd(cmd)
        print(cmd)

    def rem_bridge(self, name):
        cmd = "ovs-vsctl del-br {}".format(name)
        exec_cmd(cmd)
        print(cmd)


class Bridge(object):
    def add_port_bridge(self, list):
        bridge, port = list[0], list[1]
        cmd = "brctl addif {} {}".format(bridge, port)
        exec_cmd(cmd)
        print(cmd)


class READ(object):
    def open_file(self, file):
        with open(file) as file:
            try:
                cont = yaml.load(file, Loader=yaml.FullLoader)
                config.read_file(cont)
            except yaml.YAMLError as exc:
                print(exc)

    def read_file(self, type_config):
        for type_of_connection, interface in type_config['connection'].items():
            if type_of_connection == 'ovs-bridge':
                for i in range(len(interface)):
                    ovs.add_port_bridge(interface[i])

            if type_of_connection == 'linux-bridge':
                for i in range(len(interface)):
                    brctl.add_port_bridge(interface[i])


if __name__ == '__main__':
    ovs = OVS()
    brctl = Bridge()
    config = READ()

    file = sys.argv[1]
    config.open_file(file)
