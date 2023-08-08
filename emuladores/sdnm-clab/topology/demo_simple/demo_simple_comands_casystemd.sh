#!/bin/bash

#  docker exec clab-teste-h1 route add default gw 10.0.1.254

#  docker exec clab-teste-h2 route add default gw 10.0.2.254

  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@demo_simple_topo.json
  sleep 40
  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@demo_simple_link.json
