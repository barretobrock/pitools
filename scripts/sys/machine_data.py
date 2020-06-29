#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Log memory, cpu use and temp of each machine"""
from pitools import Sensor
from kavalkilu import Log


logg = Log('machine_data', log_to_db=True)
# Set the pin (BCM)
for sensor_name in ['CPU', 'MEM', 'CPUTEMP', 'DISK']:
    logg.debug(f'Logging {sensor_name}...')
    sensor = Sensor(sensor_name)
    # Take readings & log to db
    sensor.log_to_db(tbl=sensor_name, n_times=2)

logg.debug('Temp logging successfully completed.')

logg.close()
