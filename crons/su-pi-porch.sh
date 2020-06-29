#!/usr/bin/env bash

# VARIABLES
SENSORS=extras/pitools/scripts
PY3=/home/pi/venvs/pitools/bin/python3

# NIGHTLY REBOOT @23.57
57 23 * * * /sbin/shutdown -r now
# ENV DATA COLLECTION
*/10 * * * *    su pi    $PY3    $HOME/$SENSORS/temps/porch_temps.py
