#!/usr/bin/bash
servername=fury
SERVERNAME=${1:-$servername}
screen -p 0 -S mc-$SERVERNAME -X eval 'stuff "time query gametime"\\015'
