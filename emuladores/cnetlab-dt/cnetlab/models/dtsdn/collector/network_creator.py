import json


def create_link(devices, links, **kwargs):
    link_dic = {}

    for link in links:
        src_device, src_port = link['src']['device'], link['src']['port']
        dst_device, dst_port = link['dst']['device'], link['dst']['port']
        dst_device = devices[dst_device]['name']

        link_type, link_state = link['type'], link['state']

        # TODO:
        #  link entre spine - spine esta sendo subscrito pelo spine-cassini

        if not src_device in link_dic:
            link_dic.update({
                '{}'.format(src_device): {
                    'port {}'.format(src_port): {
                        'device': dst_device,
                        'port': dst_port,
                        'type': link_type,
                        'state': link_state,
                        'isEdgePort': False
                    }
                }
            })
        else:
            link_dic[src_device].update({
                'port {}'.format(src_port): {
                    'device': dst_device,
                    'port': dst_port,
                    'type': link_type,
                    'state': link_state,
                    'isEdgePort': False
                }
            })

        if not dst_device in link_dic:
            link_dic.update({
                '{}'.format(dst_device): {
                    'port {}'.format(dst_port): {
                        'device': src_device,
                        'port': src_port,
                        'type': link_type,
                        'state': link_state,
                        'isEdgePort': False
                    }
                }
            })
        else:
            link_dic[dst_device].update({
                'port {}'.format(dst_port): {
                    'device': src_device,
                    'port': src_port,
                    'type': link_type,
                    'state': link_state,
                    'isEdgePort': False
                }
            })

    # if len(kwargs.items()) > 0:
    if kwargs.get("edge_links"):
        edge_links = kwargs.get("edge_links")
        link_dic = create_edge_links(link_dic, edge_links)

    # print(json.dumps(link_dic, indent=2))

    return link_dic.copy()


def create_edge_links(links, edge_links):
    for device_info in edge_links:
        device_id, device_port = device_info.split('/')

        if device_id in links:
            if 'interfaces' in edge_links[device_info]:
                interfaces = edge_links[device_info]['interfaces']
                for interface in interfaces:
                    links[device_id].update({
                        'port {}'.format(device_port): {
                            'device': interface['name'],
                            'type': 'DIRECT',
                            'isEdgePort': True
                            # 'ip': interface['ips'],
                            # 'vlan': interface['vlan-untagged'],
                            # 'mac': interface['mac']
                        }
                    })

    # print(json.dumps(links, indent=2))
    return links.copy()


def add_port_statistics(device_link, ports_statistics):
    for data in ports_statistics:
        id, ports_data = data['device'], data['ports']
        if device_link[id]:
            for port_data in ports_data:
                port_name = 'port {}'.format(port_data['port'])

                if port_name in device_link[id]:
                    del port_data['port']
                    device_link[id][port_name].update({
                        'statistics': port_data
                    })

    # print(json.dumps(device_link, indent=2))

    return device_link.copy()
