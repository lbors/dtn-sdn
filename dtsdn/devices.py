
ctl_dict = {
        "dt": "172.19.1.2",
        "pd": "172.19.0.2",
    }

devices_dict = {
        "df":{
            "dt": "of:00007c55f30c1ae5",
            "pd": "of:0000eef18c8fe246",
        },
        "to":{
            "dt": "of:00004cc11cfb249f",
            "pd": "of:00003e4d6320934a",
        },
        "pa":{
            "dt": "of:00008ef91c85d09e",
            "pd": "of:0000760c19f1584b",
        },
        "ma":{
            "dt": "of:000057f1f55f2a53",
            "pd": "of:00003e3027c07048",
        },
        "pi":{
            "dt": "of:00008151c5f47647",
            "pd": "of:0000ee9d5d3a6842",
        },
        "ce":{
            "dt": "of:000075f741207305",
            "pd": "of:000052d43c1d814f",
        },
    }


class Mapa:
    def __init__(self):
        self.devices = devices_dict
        self.ctl = ctl_dict

    @property
    def devices(self):
        return self.__devices

    @devices.setter
    def devices(self, value):
        self.__devices = value

    @property
    def ctl(self):
        return self.__ctl

    @ctl.setter
    def ctl(self, value):
        self.__ctl = value

    def init(self):
        pass