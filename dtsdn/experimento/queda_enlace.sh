#!/bin/bash

  docker exec clab-whx-redeIpe-df-ht bash -c  "ping -c 60 -s 65507 -q 10.0.7.1" &
  docker exec clab-whx-redeIpe-to-ht bash -c  "ping -c 60 -s 65507 -q 10.0.7.1" &
  docker exec clab-whx-redeIpe-pi-ht bash -c  "ping -c 60 -s 65507 -q 10.0.7.1" &

  sleep 20

  echo "Consumo de um serviço"
  docker exec clab-whx-redeIpe-pa-ht bash -c "iperf3 -c 10.0.7.1 -t 40 -p 5050 -S 184" &
  docker exec clab-whx-redeIpe-ma-ht bash -c "iperf3 -c 10.0.7.1 -t 40 -p 5051" &

  sleep 20
  echo "Enlace PI-CE derrubado"
  docker exec clab-whx-redeIpe-pi bash -c "ifconfig vif2 down" 

  sleep 30
  echo "Restabelecendo enlaces"
  docker exec clab-whx-redeIpe-pi bash -c "ifconfig vif2 up"


