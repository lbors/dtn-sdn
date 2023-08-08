#!/bin/bash

  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@only_cassini_topo.json
  sleep 40
  curl -sSL --user karaf:karaf --noproxy localhost -X POST -H 'Content-Type:application/json' http://172.10.10.2:8181/onos/v1/network/configuration/ -d@only_cassini_link.json 
