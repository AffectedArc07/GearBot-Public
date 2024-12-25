#!/bin/bash
set -euo pipefail
cd /home/aa07/GearBot/dm_env
firejail --quiet --net=none --whitelist=/home/aa07/GearBot/dm_env DreamDaemon code.dmb -ultrasafe -invisible
