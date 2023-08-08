from collector import onos_request as onos


def concatenation(devices, ports_statistics, network, hosts, apps, time):
    try:
        stat_port_dict = port_stat(ports_statistics)
        # print(json.dumps(stat_port_dict, indent=2))

        # name_devices, list_stat_ports = devices['devices'], ports_statistics.get('statistics')
        apps_actives = []

        # for i in range(len(name_devices)):
        #     device, dev_stat_ports = name_devices[i], list_stat_ports[i]
        #     if device['id'] == dev_stat_ports['device']:
        #         ports = dev_stat_ports['ports']
        #         device['statistics'] = ports
        #
        #     else:
        #         device['statistics'] = None

        for i in devices['devices']:
            ports = stat_port_dict[i['id']]
            i['statistics'] = ports
            # print(json.dumps(i, indent=2))

        for app in apps['applications']:
            if app['state'] == 'ACTIVE':
                apps_actives.append(app)

        inf_dic = dict({'time': str(time), 'network': network,
                             'applications': apps_actives})
        inf_dic.update(devices)
        inf_dic.update(hosts)

        return inf_dic

    except Exception as ex:
        return False


def build_dev_key(dev_dict):
    new_dic = {}
    for i in dev_dict['devices']:
        new_dic['{}'.format(i['id'])] = i
        del i['id']

    return new_dic


def port_stat(ports_statistics):
    dev_port = {}

    for x in ports_statistics['statistics']:
        dic = ps_list_to_dict(x['ports'])
        dev_port[x['device']] = dic

    return dev_port


def ps_list_to_dict(list_ports):
    dict_port = {}
    for i in list_ports:
        dict_port['port {}'.format(i['port'])] = i
        del i['port']

    return dict_port


def db_edit():
    devices = onos.get_infos()
    list_devices = devices['devices']
    print(type(list_devices))


# if __name__ == '__main__':
#     db_edit()


