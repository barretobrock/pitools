#!/usr/bin/env bash

# VARIABLES
SENSORS=extras/pitools/scripts
PY3=/home/pi/venvs/pitools/bin/python3

# NIGHTLY REBOOT @23.57
57 23 * * * /sbin/shutdown -r now
# ENV DATA COLLECTION
*/10 * * * *        $PY3    /home/pi/$SENSORS/temps/porch_temps.py -lvl debug
