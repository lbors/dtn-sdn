import json
from requests.adapters import HTTPAdapter
from requests import Session



def make_req(ip_ctl, data_request, action, **kwargs):
    auth = ('karaf', 'karaf')
    url = "http://{}:8181/onos/v1/{}".format(ip_ctl, data_request)
    with Session() as r:
                
        if action.__eq__("delete"):
            resp = r.delete(url=url, auth=auth)

        elif action.__eq__("post"):
            j = kwargs.get('data')
            r.headers.update({"Content-Type": "application/json"})
            resp = r.post(url=url, auth=auth, data=j)

        elif action.__eq__("get"):
            r.headers.update({"Accept": "application/json"})
            resp = r.get(url=url, auth=auth)

        else:
            raise RuntimeError("action not found")
        # return resp.ok
        return resp


def get_devices(ip_ctl):
    try:
        data_request = "devices"
        ret = make_req(ip_ctl, data_request, action="get")
        if ret.status_code:
            return ret.json()
        else:
            return False

    except Exception as ex:
        return False


def get_ports_statistics(ip_ctl):
    # data_request = "statistics/ports"
    data_request = "statistics/delta/ports"
    try:
        ret = make_req(ip_ctl, data_request, action="get")
        if ret.status_code:
            return ret.json()
        else:
            return False

    except Exception as ex:
        return False


def get_ports_device_statistics(ip_ctl, id_device):
    try:
        # data_request = "/statistics/delta/ports/{}".format(id_device)
        data_request = "statistics/ports/{}".format(id_device)
        ret = make_req(ip_ctl, data_request, action="get")
        return ret.json()

    except Exception as ex:
        return False

def get_delta_ports_device_statistics(ip_ctl, id_device):
    try:
        data_request = "statistics/delta/ports/{}".format(id_device)
        ret = make_req(ip_ctl, data_request, action="get")
        return ret.json()

    except Exception as ex:
        return False

def get_application(ip_ctl):
    try:
        data_request = "applications"
        ret = make_req(ip_ctl, data_request, action="get")
        if ret.status_code:
            return ret.json()
        else:
            return False

    except Exception as ex:
        return False


def get_network(ip_ctl):
    try:
        data_request = "network/configuration"
        ret = make_req(ip_ctl, data_request, action="get")
        if ret.status_code:
            return ret.json()
        else:
            return False

    except Exception as ex:
        return False

def get_links(ip_ctl):
    try:
        data_request = "links"
        ret = make_req(ip_ctl, data_request, action="get")
        if ret.status_code:
            return ret.json()
        else:
            return False

    except Exception as ex:
        return False

def get_hosts(ip_ctl):
    try:
        data_request = "hosts"
        ret = make_req(ip_ctl, data_request, action="get")
        if ret.status_code:
            return ret.json()
        else:
            return False

    except Exception as ex:
        return False

def get_flows(ip_ctl, dev_id):
    try: 
        # data_request = "flow"
        data_request = "flows/{}".format(dev_id)
        ret = make_req(ip_ctl, data_request, action="get")
        if ret.status_code:
            return ret.json()
        else:
            return False

    except Exception as ex:
        return False
    
def post_flows(ip_ctl, api, flows):

    try:
        data_request = "flows?appId={}".format(api)
        flows = json.dumps(flows)
        ret = make_req(ip_ctl, data_request, action="post", data=flows)
        
        if ret.status_code:
            return ret.json()
        else:
            return False        
    
    except Exception as ex:
        return False