#!/bin/bash

  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.11.2:8181/onos/v1/network/configuration/ -d@topo-teste.json
  sleep 60
#  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.11.2:8181/onos/v1/network/configuration/ -d@links-teste.json
  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.11.2:8181/onos/v1/network/configuration/ -d@test-link.json
#  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.11.2:8181/onos/v1/network/configuration/ -d@spine-link.json

#  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.11.2:8181/onos/optical/intents -d@intent.json

# sudo containerlab deploy --reconfigure --topo topo.clab.yml
