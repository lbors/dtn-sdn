#!/bin/bash

  echo "Adicionando rota ht-pa"
  docker exec clab-redeIpe-ht-pa ip addr add 10.0.1.1/24 dev eth1 && docker exec clab-redeIpe-ht-pa route add default gw 10.0.1.254
  echo "Adicionando rota ht-ma"
  docker exec clab-redeIpe-ht-ma ip addr add 10.0.2.1/24 dev eth1 && docker exec clab-redeIpe-ht-ma route add default gw 10.0.2.254
  echo "Adicionando rota ht-df"
  docker exec clab-redeIpe-ht-df ip addr add 10.0.3.1/24 dev eth1 && docker exec clab-redeIpe-ht-df route add default gw 10.0.3.254
  echo "Adicionando rota ht-to"
  docker exec clab-redeIpe-ht-to ip addr add 10.0.4.1/24 dev eth1 && docker exec clab-redeIpe-ht-to route add default gw 10.0.4.254
  sleep 3

  echo "ping para o gateway ht-pa"
  docker exec clab-redeIpe-ht-pa ping -c 3 10.0.1.254
  sleep 3
  echo "ping para o gateway ht-ma"
  docker exec clab-redeIpe-ht-ma ping -c 3 10.0.2.254
  sleep 3
  echo "ping para o gateway ht-df"
  docker exec clab-redeIpe-ht-df ping -c 3 10.0.3.254
  sleep 3
  echo "ping para o gateway ht-to"
  docker exec clab-redeIpe-ht-to ping -c 3 10.0.4.254

#  echo "ping ht2 para o ht1"
#  sleep 5
#  docker exec clab-redeIpe-ht2 ping -c 10 10.0.1.1
