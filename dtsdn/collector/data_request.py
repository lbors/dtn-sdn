from datetime import datetime
from collector import creator
from controller import onos_request as onos
import json


ip_ctl = "172.19.0.2"


def get_infos():
    try:
        devices = onos.get_devices(ip_ctl)
        devices_info = devices['devices']
        # print(json.dumps(devices_info, indent=2))
        network = onos.get_network(ip_ctl)
        devices_network_config = network['devices']
        # print(json.dumps(devices_network_config, indent=2))
        device_config = creator.create_device(devices_info, devices_network_config)
        # print(json.dumps(device_config, indent=2))

        links = onos.get_links(ip_ctl)
        devices_link = links['links']
        # print(json.dumps(devices_link, indent=2))

        edge_links = network['ports']
        statistics = onos.get_ports_statistics(ip_ctl)
        ports_statistics = statistics['statistics']
        # print(json.dumps(ports_statistics, indent=2))

        device_info = creator.add_link(device_config, devices_link, ports_statistics, edge_links=edge_links)
        # device_info = creator.add_link(device_config, devices_link, ports_statistics)

        # hosts = onos.get_hosts(ip_ctl)
        # hosts = hosts['hosts']
        hosts = network['ports']
        hosts_info = creator.add_host(hosts)

        app = onos.get_application(ip_ctl)
        apps = app['applications']

        time = datetime.now()

        data = creator.create_info(device_info, hosts_info, apps, time)
        print(json.dumps(data, indent=2))

        return data.copy()

    except Exception as ex:
        return False


if __name__ == '__main__':
    x = get_infos()
    # print(x.keys())
    # print(json.dumps(x, indent=2))
    # print(x)
    # print(json.dumps(x['devices'], indent=2))
    # print(json.dumps(x['applications'], indent=2))
    # print(x['time'])
