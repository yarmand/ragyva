#!/bin/bash
# starting script to use in a docker container

function loop() {
  while true ; do
    sleep 1000
  done
}

function server(){
  python ./server.py --config config-prod.ini
}

loop