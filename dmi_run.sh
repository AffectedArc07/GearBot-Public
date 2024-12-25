#!/bin/bash
set -euo pipefail
cd /home/aa07/GearBot/dmi_env
firejail --quiet --net=none --whitelist=/home/aa07/GearBot/dmi_env DreamDaemon env.dmb -safe -invisible
