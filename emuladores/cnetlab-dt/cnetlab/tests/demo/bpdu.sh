#!bin/bash

docker exec -it ca1w ovs-vsctl set bridge xe1 other_config:forward-bpdu=true 
docker exec -it ca1w ovs-vsctl set bridge oe1 other_config:forward-bpdu=true

#docker exec -it ca2w ovs-vsctl set bridge xe1 other_config:forward-bpdu=true 
#docker exec -it ca2w ovs-vsctl set bridge oe1 other_config:forward-bpdu=true

docker exec -it ca1e ovs-vsctl set bridge xe1 other_config:forward-bpdu=true 
docker exec -it ca1e ovs-vsctl set bridge oe1 other_config:forward-bpdu=true

#docker exec -it ca2e ovs-vsctl set bridge xe1 other_config:forward-bpdu=true 
#docker exec -it ca2e ovs-vsctl set bridge oe1 other_config:forward-bpdu=true
