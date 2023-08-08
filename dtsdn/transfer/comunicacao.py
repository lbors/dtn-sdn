import json
import sys
import time

import controller.onos_request as onos
import devices
from datetime import datetime

sys.path.append('/home/lucas/Documentos/UFPA/Mestrado/DT/dtsdn')


def get_flow(ip_ctl, **kargs):
    # kargs: dev_id = dev_dt
    try:
        flows = onos.get_flows(ip_ctl, **kargs)
        return flows.copy()

    except Exception as ex:
        return False


def post_flow(ip_ctl, **kargs):
    # kargs: api = api,
    #        flows = flows
    try:
        resp = onos.post_flows(ip_ctl, **kargs)
        return resp

    except Exception as ex:
        return False


def flow_change_dev_name(flow, devs, env):
    try:
        for f in flow['flows']:
            if env == 'dt':
                if f['deviceId'] in devs:
                    f['deviceId'] = devs[f['deviceId']][env]
                else:
                    return False
            elif env == 'pd':
                if f['deviceId'] in devs['dt']:
                    f['deviceId'] = devs['pd']
                else:
                    return False
            else:
                return False
        return flow.copy()

    except Exception as ex:
        return False


def fwd_filter(flow):
    res = [f for f in flow['flows'] if (f['appId'] == "org.onosproject.fwd")]

    fwd_flow = {"flows": res}

    return fwd_flow.copy()


def send_dt_flow(flow, ctl, devs):
    env = 'dt'
    app = "org.onosproject.fwd"
    flow_new_dev_id = flow_change_dev_name(flow, devs, env)
    flows_id = post_flow(ctl[env], api=app, flows=flow_new_dev_id)

    return flows_id


def send_pd_flow(ctl, devs, flows_dt_list):
    env = 'pd'
    app = "org.onosproject.fwd"
    flows_list = []

    for name, id in devs.items():
        flows = get_flow(ctl['dt'], dev_id=id['dt'])
        only_fwd_flow_dt = fwd_filter(flows)

        if len(only_fwd_flow_dt['flows']) > 0:
            if only_fwd_flow_dt not in flows_dt_list:
                flows_dt_list.append(only_fwd_flow_dt)
                print(flows_dt_list)
                flow_dev_pd_id = flow_change_dev_name(only_fwd_flow_dt, id, env)
                flows_id = post_flow(ctl[env], api=app, flows=flow_dev_pd_id)
                flows_list.append(flows_id)

    return flows_list.copy(), flows_dt_list.copy()


def route(dev, **kargs):
    port_src = kargs.get('port_src', None)
    port_dst = kargs.get('port_dst', None)

    # flow = {
    #     "flows": [
    #         {
    #             "priority": 100,
    #             "timeout": 10,
    #             "isPermanent": False,
    #             "deviceId": "{}".format(dev),
    #             "treatment": {
    #                 "instructions": [
    #                     {
    #                         "type": "OUTPUT",
    #                         "port": "{}".format(port_dst)
    #                     }
    #                 ],
    #                 "deferred": []
    #             },
    #             "selector": {
    #                 "criteria": [
    #                     {
    #                         "type": "ETH_TYPE",
    #                         "ethType": "0x0800"
    #                     },
    #                     {
    #                         "type": "IPV4_DST",
    #                         "ip": "10.0.7.0/24"
    #                     }
    #                 ]
    #             }
    #         }
    #     ]
    # }

    flow = {
        "flows": [
            {
                "priority": 1000,
                "timeout": 100,
                "isPermanent": False,
                "deviceId": "{}".format(dev),
                "treatment": {
                    "instructions": [
                        {
                            "type": "OUTPUT",
                            "port": "{}".format(port_dst)
                        }
                    ],
                    "deferred": []
                },
                "selector": {
                    "criteria": [
                        {
                            "type": "ETH_TYPE",
                            "ethType": "0x0800"
                        },
                        {
                            "type": "IP_DSCP",
                            "ipDscp": "46"
                        }
                    ]
                }
            }
        ]}

    return flow.copy()


if __name__ == '__main__':
    devs = devices.devices_dict
    ctls = devices.ctl_dict
    flows_list = []

    with open("../flowsEx/rota_app.json") as file:
        data = json.load(file)

    # flow_test = route('pa', "3", "2")
    # # Implantar rotas no DT
    # flow_dt_ids = send_dt_flow(flow_test, ctls, devs)
    # print(flow_dt_ids)

    # time.sleep(10)

    # Recuperar rotas do DT e enviar para Prod
    while True:
        flow_pd_ids = send_pd_flow(ctls, devs, flows_list)
        # print(flow_pd_ids)
