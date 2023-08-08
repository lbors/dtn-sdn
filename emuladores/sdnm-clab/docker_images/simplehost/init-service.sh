#!/bin/bash 
function main () {

  nmstatectl set /root/network_config/$HOSTNAME.yml

}

main