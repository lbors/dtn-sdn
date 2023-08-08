from cnetlab.models.dtsdn.collector.devices import Stratum, Cassini
# from devices import *
# import devices as dv
import cnetlab.models.dtsdn.collector.network_creator as lc

import json


def create_info(devices, hosts, apps, time):
    information = {}
    list_apps = add_apps(apps)

    information.update({
        'time': str(time),
        'devices': devices,
        'hosts': hosts,
        'applications': list_apps
    })

    return information.copy()


def create_device(devices, devices_network_config):
    try:
        devices_dict = {}

        for device in devices:
            id = device['id']
            annotations = device['annotations']
            group = device['type']
            hw = device['hw']
            sw = device['sw']
            available = device['available']
            protocol = annotations['protocol']

            if annotations['driver'] == 'stratum-bmv2':
                driver = annotations['driver']
                name, pipeconf, address, \
                    edge_router, mgm_address, \
                    nodeSid, routerMac = Stratum.network_config(devices_network_config[id])
                globals()[f"{name}"] = Stratum(id, name, address, group=group, hw=hw, sw=sw, available=available,
                                               protocol=protocol, pipeconf=pipeconf, driver=driver,
                                               edge_router=edge_router, mgm_address=mgm_address,
                                               node_sid=nodeSid, router_mac=routerMac)

            if annotations['driver'] == 'cassini-openconfig':
                name = annotations['name']
                driver = device['driver']
                address = annotations['ipaddress']
                username, password, port, mgm_address = Cassini.network_config(devices_network_config[id])

                globals()[f"{name}"] = Cassini(id, name, address, group=group, hw=hw, sw=sw, available=available,
                                               protocol=protocol, driver=driver, username=username,
                                               password=password, port=port, mgm_address=mgm_address)

            device_dict = globals()[f"{name}"].dic_device_config()
            devices_dict.update({id: device_dict})

        # print(list_variables)
        # print(json.dumps(name_devices, indent=2))

        # return name_devices
        return devices_dict.copy()

    except Exception as ex:
        return False


def add_host(hosts, ports):
    hosts_dict = {}
    # print(ports)

    for host in hosts:
        try:
            host_loc = host['locations'][0]
            device, device_port = host_loc['elementId'],  host_loc['port']
            device_key = "{}/{}".format(device, device_port)
            interface = ports[device_key]['interfaces'][0]

            host_name = interface['name']
            ip_host = host['ipAddresses'][0]
            gateway, cidr = interface['ips'][0].split('/')

            if host['vlan'] == 'None':
                vlan = 'vlan-untagged'
                vlan_number = interface['vlan-untagged']
            else:
                pass

            hosts_dict.update({
                "{}".format(host_name): {
                    'name': host_name,
                    'ip': ip_host,
                    'cidr': cidr,
                    'gw': gateway,
                    'vlan': vlan,
                    'vlan_number': vlan_number,
                    'mac': interface['mac'],
                    'device': device,
                    'port': device_port,
                }
            })
        except Exception as ex:
            pass

    # print(json.dumps(hosts_dict, indent=2))

    return hosts_dict.copy()


def add_link(devices, devices_link, ports_statistics, **kwargs):

    link = lc.create_link(devices, devices_link, **kwargs)
    link_complete = lc.add_port_statistics(link, ports_statistics)

    for device in devices:
        devices[device].update({
            'links': link_complete[device]
        })

    # print(json.dumps(devices.copy(), indent=2))

    return devices.copy()


def add_apps(apps):
    apps_actives = []
    for app in apps:
        if app['state'] == 'ACTIVE':
            apps_actives.append(app)

    # print(json.dumps(apps_actives, indent=2))

    return apps_actives

