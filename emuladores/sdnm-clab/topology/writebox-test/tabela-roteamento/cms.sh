#!/bin/bash

# docker exec clab-whx-teste-whx1 bash -c "ovs-vsctl add-br br0 ; \
# ovs-vsctl set bridge br0 other_config:name=whx1 ; \
# ovs-vsctl set bridge br0 other_config:datapath-id=of:0000000000000001 ; \
# ovs-vsctl set bridge br0 protocols=OpenFlow13 ; \
# ovs-vsctl set-controller br0 tcp:172.10.10.2:6653 ; \
# ovs-vsctl add-port br0 vif1 ; \
# ovs-vsctl add-port br0 vif2 ; \
# ovs-vsctl add-port br0 ht1"

# docker exec clab-whx-teste-whx2 bash -c "ovs-vsctl add-br br0 ; \
# ovs-vsctl set bridge br0 other_config:name=whx2 ; \
# ovs-vsctl set bridge br0 other_config:datapath-id=of:0000000000000002 ; \
# ovs-vsctl set bridge br0 protocols=OpenFlow13 ; \
# ovs-vsctl set-controller br0 tcp:172.10.10.2:6653 ; \
# ovs-vsctl add-port br0 vif1 ; \
# ovs-vsctl add-port br0 vif2 ; \
# ovs-vsctl add-port br0 ht2 ; \
# ovs-vsctl add-port br0 ht3"

#-------

docker exec clab-whx-teste-ht1 bash -c "ip addr add 10.0.1.1/24 dev eth1 ; ip route add 10.0.1.0/24 dev eth1 ; ip route add 10.0.2.0/24 dev eth1 ; ip route add 10.0.3.0/24 dev eth1"

docker exec clab-whx-teste-ht2 bash -c "ip addr add 10.0.2.1/24 dev eth1 ; ip route add 10.0.1.0/24 dev eth1 ; ip route add 10.0.2.0/24 dev eth1 ; ip route add 10.0.3.0/24 dev eth1"

docker exec clab-whx-teste-ht3 bash -c "ip addr add 10.0.3.1/24 dev eth1 ; ip route add 10.0.1.0/24 dev eth1 ; ip route add 10.0.2.0/24 dev eth1 ; ip route add 10.0.3.0/24 dev eth1"

#-------

#curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/flows?appId=org.onosproject.fwd -d@flows/flows-ht1-ht2-ht3.json



