#!/bin/bash

  docker exec clab-teste-ca1 ovs-vsctl add-port oe1 ca1-ovif1 && docker exec clab-teste-ca1 ovs-vsctl add-port xe1 ca1-vif1
  docker exec clab-teste-ca2 ovs-vsctl add-port oe1 ca2-ovif1 && docker exec clab-teste-ca2 ovs-vsctl add-port xe1 ca2-vif1

  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@only_cassini_topo.json
  sleep 40
  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@only_cassini_link.json