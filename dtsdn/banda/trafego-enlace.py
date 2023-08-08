# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2023 National Network for Education and Research (RNP)        +
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

import sys
from controller import onos_request as ctl
import devices
import time
import threading
import transfer.comunicacao as cmc

sys.path.append('/home/lucas/Documentos/UFPA/Mestrado/DT/dtsdn')


def bit_rate_gb(bytes_sent):
    gigabits = (bytes_sent / 8) / 1000000000
    return gigabits


def capacidade_enlace(banda_disponivel, banda_usada):
    largura_banda_utilizada = (banda_usada / banda_disponivel) * 100
    return largura_banda_utilizada


def get_status_port(port):
    pass


def get_stat_port(ctls, dev, env, name):
    dict_delta = ctl.get_delta_ports_device_statistics(ctls[env], dev[env])
    delta_ports = dict_delta['statistics'][0]["ports"]
    sat_saida = 1
    sat_chegada = 0.1

    list_stat = []
    for port in delta_ports:
        if port['port'] is not len(delta_ports):  # Ultima porta é reservada ao host, entao ela é desconsiderada
            taxa_gb_recebido = bit_rate_gb(port["bytesReceived"])  # Chega na porta
            taxa_gb_enviado = bit_rate_gb(port["bytesSent"])  # Sai na porta
            # print(port['port'], taxa_gb_recebido, taxa_gb_enviado)

            if taxa_gb_enviado <= 0 or taxa_gb_recebido <= 0:  # Link caido
                list_stat.append((name, (port['port'], "undefined", "undefined"), (taxa_gb_recebido, taxa_gb_enviado)))
            elif taxa_gb_enviado > taxa_gb_recebido:
                if taxa_gb_enviado > sat_saida:
                    list_stat.append(
                        (name, (port['port'], "sentLink", "saturado"), (taxa_gb_recebido, taxa_gb_enviado)))
                else:
                    list_stat.append((name, (port['port'], "sentLink", "normal"), (taxa_gb_recebido, taxa_gb_enviado)))
            elif taxa_gb_recebido > taxa_gb_enviado:
                if taxa_gb_recebido > sat_chegada:
                    list_stat.append(
                        (name, (port['port'], "reseivedLink", "saturado"), (taxa_gb_recebido, taxa_gb_enviado)))
                else:
                    list_stat.append(
                        (name, (port['port'], "reseivedLink", "normal"), (taxa_gb_recebido, taxa_gb_enviado)))
            else:
                list_stat.append((name, (port['port'], "reseivedLink", "normal"), (taxa_gb_recebido, taxa_gb_enviado)))
    return list_stat.copy()


def def_new_route(ctl, dev_id, stat, name):
    env = "dt"

    for i in range(1, len(stat) + 1):  # Indice da lista difere do laço em -1 unidade
        device = stat[i - 1][0]  # Nome dispositivo
        port = stat[i - 1][1][0]  # Numero da porta
        port_type = stat[i - 1][1][1]  # sentLink (Uplink), reseivedLink (Downlink) ou undefined
        port_status = stat[i - 1][1][2]  # Saturada, normal ou undefined

        stat_port_recebido = stat[i - 1][2][0]  # Trafego de entrada
        stat_port_enviado = stat[i - 1][2][1]  # Trafego de saida

        # print(device, port, port_type, port_status, stat_port_recebido, stat_port_enviado)

        if port_status == "saturado" and port_type == "sentLink":
            # print(device, port, port_type, port_status, stat_port_recebido, stat_port_enviado)
            if port == 1:
                for j in range(port + 1, len(stat) + 1):
                    if stat[j - 1][1][1] == "reseivedLink" and stat[j - 1][1][2] != "saturado":
                        port_dst = stat[j - 1][1][0]
                        print("1º", device, port_dst, stat)

                        return port_dst, dev_id[env], name

            elif 1 < port < len(stat):
                for j in range(port - 1, 1, -1):
                    if stat[j-1][1][1] == "reseivedLink" and stat[j-1][1][2] != "saturado":
                        port_dst = stat[j - 1][1][0]
                        print("2º", device, port_dst, stat)

                        return port_dst, dev_id[env], name

                for j in range(port + 1, len(stat) + 1):
                    if stat[j - 1][1][1] == "reseivedLink" and stat[j - 1][1][2] != "saturado":
                        port_dst = stat[j - 1][1][0]
                        print("3º", device, port_dst, stat)

                        return port_dst, dev_id[env], name

            elif port == len(stat):
                for j in range(port - 1, 0, -1):
                    # print(j, stat[j][1][1], stat[j][1][2], stat[j][2][0], stat[j][2][1], stat[j][1][0])
                    if stat[j - 1][1][1] == "reseivedLink" and stat[j - 1][1][2] != "saturado":
                        port_dst = stat[j - 1][1][0]
                        print("4º", device, port_dst, stat)

                        return port_dst, dev_id[env], name

        elif port_status == "undefined":
            if port == 1:
                for j in range(port + 1, len(stat) + 1):
                    if 0 < stat[j - 1][2][0] < 0.001:
                        port_dst = stat[j - 1][1][0]
                        print("5º", device, port_dst, stat)

                        return port_dst, dev_id[env], name

            elif 1 < port < len(stat):
                for j in range(port - 1, 1, -1):
                    if 0 < stat[j-1][2][0] < 0.001:
                        port_dst = stat[j - 1][1][0]
                        print("6º", device, port_dst, stat)

                        return port_dst, dev_id[env], name

                for j in range(port + 1, len(stat) + 1):
                    if 0 < stat[j - 1][2][0] < 0.001:
                        port_dst = stat[j - 1][1][0]
                        print("7º", device, port_dst, stat)

                        return port_dst, dev_id[env], name

            elif port == len(stat):
                for j in range(port - 1, 0, -1):
                    if 0 < stat[j - 1][2][0] < 0.001:
                        port_dst = stat[j - 1][1][0]
                        print("8º", device, port_dst, stat)

                        return port_dst, dev_id[env], name


def acoes(ctls, name, id, env, role_list):
    statistics = get_stat_port(ctls, id, env, name)
    # print(statistics)
    data = def_new_route(ctls, devs[name], statistics, name)
    # print(data)
    if data is not None:
        flow = cmc.route(data[1], port_dst=data[0])
        flow_dt_id = cmc.post_flow(ctls['dt'], api="org.onosproject.fwd", flows=flow)
        print(data, flow_dt_id)

        role_list.append(data)

        # if data not in role_list:
            # print(data)
            # flow = cmc.route(data[1], port_dst=data[0])
            # flow_dt_id = cmc.post_flow(ctls['dt'], api="org.onosproject.fwd", flows=flow)
            # print(flow_dt_id)
            #
            # role_list.append(data)

        # try:
        #     element = list.index(data)
        #     print(element)
        # except:
        #     print(data)
        #     flow = cmc.route(data[1], port_dst=data[0])
        #     flow_dt_id = cmc.post_flow(ctls['pd'], api="org.onosproject.fwd", flows=flow)
        #     print(flow_dt_id)
        #
        #     role_list.append(data)


def check_device(ctls, dev_ids, dev_env, list, **kargs):
    if len(dev_ids) <= 2:
        dev_name = kargs.get('dev_name', None)
        acoes(ctls, dev_name, dev_ids, dev_env, list)

    else:
        for dev_name, dev_ids in devices.devices_dict.items():
            if dev_name != "ce":
                get_port_info = threading.Thread(target=acoes, args=(ctls, dev_name, dev_ids, dev_env, list))
                get_port_info.start()
                # acoes(ctls, dev_name, dev_ids, dev_env, list)



if __name__ == '__main__':
    devs = devices.devices_dict
    ctls = devices.ctl_dict
    env = "pd"
    role_list = []

    while True:
        check_device(ctls, devs, env, role_list)
        # check_device(ctls, devs['ma'], "pd", role_list, dev_name='ma')
        time.sleep(1)
