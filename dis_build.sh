#!/bin/bash
set -euo pipefail
cd /home/aa07/GearBot/src
firejail --quiet --net=none --whitelist=/home/aa07/GearBot/src DreamMaker code.dm
