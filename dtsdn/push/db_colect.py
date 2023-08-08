from influxdb_client import InfluxDBClient
from influxdb_client.client.flux_table import FluxStructureEncoder
import json

token = "q0U6qAjXfAhEOS-HsF-t1Mxx8rChTz_BUCBFsdyoCcqdnj-S0hFsOMvP8sJC9-EsTLFpLyCDqQvaGjKWIfL0dg=="
org = "onos"
bucket = "onos"
url = "http://172.19.0.2:8086"
client = InfluxDBClient(url=url, token=token, org=org)


def read_apps():
    query_apps = 'from(bucket: "onos")' \
                 '|> range(start: -10s)' \
                 '|> filter(fn: (r) => r["_measurement"] == "Applications")' \
                 '|> filter(fn: (r) => r["state"] == "ACTIVE")' \
                 '|> keep(columns: ["name"])' \
                 '|> distinct(column: "name")'

    records = client.query_api().query(query_apps, org=org)
    output = json.dumps(records, cls=FluxStructureEncoder, indent=2)

    return output


def read_links():
    query_links = 'from (bucket: "onos")' \
                  '|> range(start: -10s)' \
                  '|> filter(fn: (r) => r["_measurement"] == "Links")' \
                  '|> filter(fn: (r) => r["status"] == "ACTIVE")' \
                  '|> keep(columns: ["device_src", "port_src", "device_dst", "port_dst", "type"])' \
                  '|> distinct(column: "device_src")'

    records = client.query_api().query(query_links, org=org)

    output = json.dumps(records, cls=FluxStructureEncoder, indent=2)
    # print(output)

    return output


def read_devices():
    query_devices = 'from (bucket: "onos")' \
                    '|> range(start: -10s)' \
                    '|> filter(fn: (r) => r["_measurement"] == "Informations")' \
                    '|> filter(fn: (r) => r["status"] == "True")' \
                    '|> keep(columns: ["device", "name", "type", "driver", "pipeconf", "latitude", "longitude"])' \
                    '|> distinct(column: "device")'

    records = client.query_api().query(query_devices, org=org)

    output = json.dumps(records, cls=FluxStructureEncoder, indent=2)
    # print(output)

    return output


def create_devices():
    list_data = json.loads(read_devices())
    list_config = []

    for devices in list_data:
        for device in devices['records']:
            # print(device)
            data = device['values']

            device_id = data['device']
            device_name = data['name']
            device_driver = data['driver']
            device_pipeconf = data['pipeconf']
            device_lat = data['latitude']
            device_long = data['longitude']

            config = (device_id, device_name, device_driver, device_pipeconf, device_lat, device_long)

            list_config.append(config)

    return list_config


def create_links():
    list_data = json.loads(read_links())
    list_link = []

    for data in list_data:
        for link in data['records']:
            values = link['values']
            # print(values)
            # print("src: {}/{} - dst: {}/{}".format(values['device_src'], values['port_src'],
            #                                        values['device_dst'], values['port_dst']))
            x = (values['device_src'], values['device_dst'], values['type'])

            list_link.append(x)

    return list_link[::-1]


def set_app():
    list_data = json.loads(read_apps())
    list_app = []

    for apps in list_data:
        for app in apps['records']:
            values = app['values']
            name = values['name']
            name = name.replace("org.onosproject.", "")

            list_app.append(name)

    return list_app




# with InfluxDBClient(url=url, token=token, org=org) as client:
#     query_api = client.query_api()

    # record = read_apps()
    # record = read_links()
    # record = read_devices()
    # print(create_devices())
    # print(create_links())
    # print(set_app())


if __name__ == "__main__":
    # print(set_app())
    # print(create_links())
    print(create_devices())

