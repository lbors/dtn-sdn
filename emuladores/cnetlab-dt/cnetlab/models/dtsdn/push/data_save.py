# import influxdb_client
import time

from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient
from collector import onos_request as dc


def write_statistics():
    devices = data['devices']

    for device in devices:
        dev = device['statistics']
        '''
            "port x": {
                "packetsReceived": ,
                "packetsSent": ,
                "bytesReceived": ,
                "bytesSent": ,
                "packetsRxDropped": ,
                "packetsTxDropped": ,
                "packetsRxErrors": ,
                "packetsTxErrors": ,
                "durationSec": 
              },
        '''

        for dev_port, port_sta in dev.items():
            # print(json.dumps(inf, indent=2))
            conteudo = {
                "times": times,
                "measurement": "Statistics",
                "tags": {
                    "device": device['id'],
                    "port": dev_port
                },
                "fields": port_sta
            }
            json_payload.append(conteudo)

    # print(json.dumps(json_payload, indent=2))


def write_info():
    devices = data["devices"]

    for device in devices:
        annot = device['annotations']
        id = device['id']
        name = annot['name']
        name = name.replace("device:", "")
        type = device['type']
        status = device['available']
        mfr = device['mfr']
        hw = device['hw']
        sw = device['sw']
        lat = annot['latitude']
        long = annot['longitude']
        protocol = annot['protocol']

        driver = device['driver']
        pipeconf = " "
        if driver == "stratum-bmv2:org.onosproject.pipelines.fabric":
            driver, pipeconf = driver.split(":")

        if annot['protocol'] == 'NETCONF':
            mgmAddress = annot['ipaddress']
        else:
            mgmAddress = annot['managementAddress']


        conteudo = {
            "times": times,
            "measurement": "Informations",
            "tags": {
                "device": id,
                "name": name,
                "type": type,
                "status": status,
                "driver": driver,
                "pipeconf": pipeconf,
                "managementAddress": mgmAddress,
                "latitude": lat,
                "longitude": long
            },
            "fields": {
                "mfr": mfr,
                "hw": hw,
                "sw": sw,
                "protocol": protocol
            }
        }

        json_payload.append(conteudo)

    # print(json.dumps(json_payload, indent=2))


def write_app():
    apps = data['applications']

    for app in apps:
        name = app['name']
        state = app['state']
        category = app['category']

        conteudo = {
            "times": times,
            "measurement": "Applications",
            "tags": {
                "name": name,
                "state": state
            },
            "fields": {
                "category": category
            }
        }

        json_payload.append(conteudo)


def write_links():
    network = data['network']
    links = network['links']

    '''
        "id/port-id/port": {
            "basic": {
                "type": "DIRECT",
                "metric": 1,
                "durable": true,
                "bidirectional": true
            }
        }
    '''

    for device, info in links.items():
        dev_src, dev_dst = device.split('-')
        dev_src = dev_src.split('/')
        dev_dst = dev_dst.split('/')
        conf = info['basic']

        conteudo = {
            "times": times,
            "measurement": "Links",
            "tags": {
                "status": "ACTIVE",
                "device_src": dev_src[0],
                "port_src": dev_src[1],
                "device_dst": dev_dst[0],
                "port_dst": dev_dst[1],
                "type": conf['type']
            },
            "fields": {
                "type": conf['type']
            }
        }
        json_payload.append(conteudo)
    # print(json.dumps(json_payload, indent=2))

token = "q0U6qAjXfAhEOS-HsF-t1Mxx8rChTz_BUCBFsdyoCcqdnj-S0hFsOMvP8sJC9-EsTLFpLyCDqQvaGjKWIfL0dg=="
org = "onos"
bucket = "onos"

with InfluxDBClient(url="http://172.19.0.2:8086", token=token, org=org) as client:

    while True:
        json_payload = []
        data = dc.get_infos()
        times = data['time']

        write_info()
        write_statistics()
        write_links()
        write_app()

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, json_payload)

        # print(json.dumps(json_payload, indent=2))

        time.sleep(1)

    # json_payload = []
    # data = dc.get_infos()
    # times = data['time']
    # write_info()
    # print(json.dumps(json_payload, indent=2))