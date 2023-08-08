class Devices(object):
    def __init__(self, id, name, address, **params):
        self._id = id
        self._name = name
        self._address = address
        self._group = params.get('group', None)
        self._hw = params.get('hw', None)
        self._sw = params.get('sw', None)
        self._available = params.get('available', None)
        self._driver = params.get('driver', None)
        self._protocol = params.get('protocol', None)
        self._mgm_address = params.get('mgm_address', None)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def group(self):
        return self._group

    @group.setter
    def type(self, value):
        self._group = value

    @property
    def hw(self):
        return self._hw

    @hw.setter
    def hw(self, value):
        self._hw = value

    @property
    def sw(self):
        return self._sw

    @sw.setter
    def sw(self, value):
        self._sw = value

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        self._available = value

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._protocol = value

    @property
    def mgm_address(self):
        return self._mgm_address

    @mgm_address.setter
    def mgm_address(self, value):
        self._mgm_address = value

    def dic_device_config(self):
        conf = dict()
        conf.update({
            "name": self.name,
            "driver": self.driver,
            "group": self.group,
            "hw": self.hw,
            "sw": self.sw,
            "available": self.available,
            "protocol": self.protocol
        })
        return conf.copy()

    def device_ports(self):
        pass


class Stratum(Devices):
    def __init__(self, id, name, address, **params):
        super().__init__(id, name, address, **params)
        self._pipeconf = params.get('pipeconf', None)
        self._edge_router = params.get('edge_router', None)

    @property
    def pipeconf(self):
        return self._pipeconf

    @pipeconf.setter
    def pipeconf(self, value):
        self._pipeconf = value

    @property
    def edge_router(self):
        return self._edge_router

    @edge_router.setter
    def edge_router(self, value):
        self._edge_router = value

    def dic_device_config(self):
        dic = super(Stratum, self).dic_device_config()
        dic.update({
            "pipeconf": self.pipeconf,
            "network": {
                "address": self.address,
                "isEdgeRouter": self.edge_router,
                "managementAddress": self.mgm_address
            }
        })

        return dic.copy()

    def network_config(device):
        routing = device['segmentrouting']
        basic = device['basic']

        name = routing['name']
        # ipv4NodeSid = routing['ipv4NodeSid']
        address = routing['ipv4Loopback']
        # routerMac = routing['routerMac']
        edgeRouter = routing['isEdgeRouter']

        pipeconf = basic['pipeconf']
        mgmAddress = basic['managementAddress']

        return name, pipeconf, address, edgeRouter, mgmAddress


class Cassini(Devices):
    def __init__(self, id, name, address, **params):
        super(Cassini, self).__init__(id, name, address, **params)
        self._username = params.get('username', None)
        self._password = params.get('password', None)
        self._port = params.get('port', None)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    def dic_device_config(self):
        dic = super(Cassini, self).dic_device_config()
        dic.update({
            "network": {
                "username": self.username,
                "password": self.password,
                "port": self.port,
                "managementAddress": self.mgm_address
            }
        })

        return dic.copy()

    def network_config(device):
        netconf = device['netconf']
        username = netconf['username']
        password = netconf['password']
        port = netconf['port']
        mgmAddress = netconf['ip']

        return username, password, port, mgmAddress

# https://www.programiz.com/python-programming/property
# https://realpython.com/python-property/
