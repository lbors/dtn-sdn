from datetime import datetime
from cnetlab.models.dtsdn.collector import creator, onos_request as onos
import json


ip_ctl = "172.19.0.2"


def get_infos(ip_ctl):
    try:
        devices = onos.get_devices(ip_ctl)
        devices_info = devices['devices']
        network = onos.get_network(ip_ctl)
        devices_network_config = network['devices']
        device_config = creator.create_device(devices_info, devices_network_config)

        links = onos.get_links(ip_ctl)
        devices_link = links['links']

        edge_links = network['ports']
        statistics = onos.get_ports_statistics(ip_ctl)
        ports_statistics = statistics['statistics']

        device_info = creator.add_link(device_config, devices_link, ports_statistics, edge_links=edge_links)
        # device_info = creator.add_link(device_config, devices_link, ports_statistics)

        hosts = onos.get_hosts(ip_ctl)
        hosts = hosts['hosts']
        ports = network['ports']
        hosts_info = creator.add_host(hosts, ports)

        app = onos.get_application(ip_ctl)
        apps = app['applications']

        time = datetime.now()

        data = creator.create_info(device_info, hosts_info, apps, time)
        # print(json.dumps(data, indent=2))

        return data.copy()

    except Exception as ex:
        return False


if __name__ == '__main__':
    x = get_infos(ip_ctl)
    # print(x.keys())
    # print(json.dumps(x, indent=2))
    # print(x)
    # print(json.dumps(x['devices'], indent=2))
    # print(json.dumps(x['applications'], indent=2))
    # print(x['time'])
