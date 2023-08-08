#!/bin/bash

  docker exec clab-teste-ca1 ovs-vsctl add-port oe1 ca1-ovif1 && docker exec clab-teste-ca1 ovs-vsctl add-port xe1 ca1-vif1
  docker exec clab-teste-ca2 ovs-vsctl add-port oe1 ca2-ovif1 && docker exec clab-teste-ca2 ovs-vsctl add-port xe1 ca2-vif1

  docker exec clab-teste-leaf1 brctl addif port1 leaf1-vif1 && docker exec clab-teste-leaf1 brctl addif port2 leaf1-vif2
  docker exec clab-teste-leaf2 brctl addif port1 leaf2-vif1 && docker exec clab-teste-leaf2 brctl addif port2 leaf2-vif2

  docker exec clab-teste-spine1 brctl addif port1 spine1-vif1 && docker exec clab-teste-spine1 brctl addif port2 spine1-vif2
  docker exec clab-teste-spine2 brctl addif port1 spine2-vif1 && docker exec clab-teste-spine2 brctl addif port2 spine2-vif2

#  docker exec clab-teste-h1 ip addr add 10.0.1.1/24 dev ht1-ht1
  docker exec clab-teste-h1 route add default gw 10.0.1.254

#  docker exec clab-teste-h2 ip addr add 10.0.2.1/24 dev ht2-ht1
  docker exec clab-teste-h2 route add default gw 10.0.2.254

  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@demo_simple_topo.json 
  sleep 40
  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@demo_simple_link.json 
