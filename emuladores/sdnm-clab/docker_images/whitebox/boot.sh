#!/bin/sh
export PATH=$PATH:/usr/share/openvswitch/scripts/
ovs-ctl --system-id=random start

sleep 10

python3 /home/config-ports.py

sleep 60

ovs-vsctl set bridge br0 protocols=OpenFlow13 ; ovs-vsctl set-controller br0 tcp:$IP_CTL:6653

/bin/sh