#!/usr/bin/env bash

# VARIABLES
SENSORS=extras/pitools/scripts
PY3=/home/pi/venvs/pitools/bin/python3

# LOG ANALYSIS
#0 */4 * * *     $PY3    $HOME/$SENSORS/log_reader.py
#32 3 20 * *     $PY3    $HOME/$SENSORS/log_remover.py -lvl debug
# ENV DATA COLLECTION
*/10 * * * *    $PY3    $HOME/$SENSORS/sys/machine_data.py -lvl debug
