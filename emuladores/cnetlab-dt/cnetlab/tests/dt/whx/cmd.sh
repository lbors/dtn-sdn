#!/bin/bash

docker exec df-ht ping -c 1 10.0.2.254 ; docker exec to-ht ping -c 1 10.0.3.254 ; docker exec pa-ht ping -c 1 10.0.4.254 ; docker exec ma-ht ping -c 1 10.0.5.254 ; docker exec pi-ht ping -c 1 10.0.6.254 ; docker exec ce-ht ping -c 1 10.0.7.254


docker exec df-ht bash -c "ip route add 10.0.2.0/24 dev df-ht-ht1 ; ip route add 10.0.3.0/24 dev df-ht-ht1 ; ip route add 10.0.4.0/24 dev df-ht-ht1 ; ip route add 10.0.5.0/24 dev df-ht-ht1 ; ip route add 10.0.6.0/24 dev df-ht-ht1 ; ip route add 10.0.7.0/24 dev df-ht-ht1"

docker exec to-ht bash -c "ip route add 10.0.2.0/24 dev to-ht-ht1 ; ip route add 10.0.3.0/24 dev to-ht-ht1 ; ip route add 10.0.4.0/24 dev to-ht-ht1 ; ip route add 10.0.5.0/24 dev to-ht-ht1 ; ip route add 10.0.6.0/24 dev to-ht-ht1 ; ip route add 10.0.7.0/24 dev to-ht-ht1"

docker exec pa-ht bash -c "ip route add 10.0.2.0/24 dev pa-ht-ht1 ; ip route add 10.0.3.0/24 dev pa-ht-ht1 ; ip route add 10.0.4.0/24 dev pa-ht-ht1 ; ip route add 10.0.5.0/24 dev pa-ht-ht1 ; ip route add 10.0.6.0/24 dev pa-ht-ht1 ; ip route add 10.0.7.0/24 dev pa-ht-ht1"

docker exec ma-ht bash -c "ip route add 10.0.2.0/24 dev ma-ht-ht1 ; ip route add 10.0.3.0/24 dev ma-ht-ht1 ; ip route add 10.0.4.0/24 dev ma-ht-ht1 ; ip route add 10.0.5.0/24 dev ma-ht-ht1 ; ip route add 10.0.6.0/24 dev ma-ht-ht1 ; ip route add 10.0.7.0/24 dev ma-ht-ht1"

docker exec pi-ht bash -c "ip route add 10.0.2.0/24 dev pi-ht-ht1 ; ip route add 10.0.3.0/24 dev pi-ht-ht1 ; ip route add 10.0.4.0/24 dev pi-ht-ht1 ; ip route add 10.0.5.0/24 dev pi-ht-ht1 ; ip route add 10.0.6.0/24 dev pi-ht-ht1 ; ip route add 10.0.7.0/24 dev pi-ht-ht1"

docker exec ce-ht bash -c "ip route add 10.0.2.0/24 dev ce-ht-ht1 ; ip route add 10.0.3.0/24 dev ce-ht-ht1 ; ip route add 10.0.4.0/24 dev ce-ht-ht1 ; ip route add 10.0.5.0/24 dev ce-ht-ht1 ; ip route add 10.0.6.0/24 dev ce-ht-ht1 ; ip route add 10.0.7.0/24 dev ce-ht-ht1"