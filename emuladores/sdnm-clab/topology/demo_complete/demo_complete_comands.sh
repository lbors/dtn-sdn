#!/bin/bash

  docker exec clab-demo-ca1w ovs-vsctl add-port oe1 ca1w-ovif1 && docker exec clab-demo-ca1w ovs-vsctl add-port xe1 ca1w-vif1
  docker exec clab-demo-ca2w ovs-vsctl add-port oe1 ca2w-ovif1 && docker exec clab-demo-ca2w ovs-vsctl add-port xe1 ca2w-vif1

  docker exec clab-demo-ca1e ovs-vsctl add-port oe1 ca1e-ovif1 && docker exec clab-demo-ca1e ovs-vsctl add-port xe1 ca1e-vif1
  docker exec clab-demo-ca2e ovs-vsctl add-port oe1 ca2e-ovif1 && docker exec clab-demo-ca2e ovs-vsctl add-port xe1 ca2e-vif1

  docker exec clab-demo-spine_w1 brctl addif port1 spine_w1-vif1 && docker exec clab-demo-spine_w1 brctl addif port2 spine_w1-vif2 && docker exec clab-demo-spine_w1 brctl addif port3 spine_w1-vif3
  docker exec clab-demo-spine_w2 brctl addif port1 spine_w2-vif1 && docker exec clab-demo-spine_w2 brctl addif port2 spine_w2-vif2 && docker exec clab-demo-spine_w2 brctl addif port3 spine_w2-vif3

  docker exec clab-demo-spine_e1 brctl addif port1 spine_e1-vif1 && docker exec clab-demo-spine_e1 brctl addif port2 spine_e1-vif2 && docker exec clab-demo-spine_e1 brctl addif port3 spine_e1-vif3
  docker exec clab-demo-spine_e2 brctl addif port1 spine_e2-vif1 && docker exec clab-demo-spine_e2 brctl addif port2 spine_e2-vif2 && docker exec clab-demo-spine_e2 brctl addif port3 spine_e2-vif3

  docker exec clab-demo-leaf_w1 brctl addif port1 leaf_w1-vif1 && docker exec clab-demo-leaf_w1 brctl addif port2 leaf_w1-vif2 && docker exec clab-demo-leaf_w1 brctl addif port3 leaf_w1-vif3
  docker exec clab-demo-leaf_w2 brctl addif port1 leaf_w2-vif1 && docker exec clab-demo-leaf_w2 brctl addif port2 leaf_w2-vif2 && docker exec clab-demo-leaf_w2 brctl addif port3 leaf_w2-vif3

  docker exec clab-demo-leaf_e1 brctl addif port1 leaf_e1-vif1 && docker exec clab-demo-leaf_e1 brctl addif port2 leaf_e1-vif2 && docker exec clab-demo-leaf_e1 brctl addif port3 leaf_e1-vif3
  docker exec clab-demo-leaf_e2 brctl addif port1 leaf_e2-vif1 && docker exec clab-demo-leaf_e2 brctl addif port2 leaf_e2-vif2 && docker exec clab-demo-leaf_e2 brctl addif port3 leaf_e2-vif3


  docker exec clab-demo-dtn1 ip addr add 10.0.1.1/24 dev dtn1-ht1 && docker exec clab-demo-dtn1 route add default gw 10.0.1.254

  docker exec clab-demo-dtn2 ip addr add 10.0.2.1/24 dev dtn2-ht1 && docker exec clab-demo-dtn2 route add default gw 10.0.2.254

  docker exec clab-demo-dtn3 ip addr add 10.0.3.1/24 dev dtn3-ht1 && docker exec clab-demo-dtn3 route add default gw 10.0.3.254

  docker exec clab-demo-dtn4 ip addr add 10.0.4.1/24 dev dtn4-ht1 && docker exec clab-demo-dtn4 route add default gw 10.0.4.254


  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@demo_complete_device.json

  sleep 60

  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@demo_complete_link.json
