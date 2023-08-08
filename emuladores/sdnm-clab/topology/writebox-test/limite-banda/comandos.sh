#!/bin/bash


docker exec clab-whx-teste-ht1 bash -c "ip addr add 10.0.1.2/24 dev eth1 ; ip route add 10.0.1.0/24 dev eth1 ; ip route add 10.0.2.0/24 dev eth1 ; ping -c 1 10.0.1.254"

docker exec clab-whx-teste-ht2 bash -c "ip addr add 10.0.2.2/24 dev eth1 ; ip route add 10.0.1.0/24 dev eth1 ; ip route add 10.0.2.0/24 dev eth1 ; ping -c 1 10.0.2.254"


#-------
# Taxa 10Gbps
# ovs-vsctl set interface vif1 ingress_policing_rate=10000000 ; ovs-vsctl set interface vif1 ingress_policing_burst=1000000

# Taxa 10Mbps
# ovs-vsctl set interface vif1 ingress_policing_rate=10000 ; ovs-vsctl set interface vif1 ingress_policing_burst=10000

#curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/flows?appId=org.onosproject.fwd -d@flows/tipo-pacote.json



