#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Log memory, cpu use and temp of each machine"""
from kavalkilu import LogWithInflux, InfluxDBHomeAuto
from pitools import Sensor


logg = LogWithInflux('machine_data')
# Set the pin (BCM)
for sensor_name in ['CPU', 'MEM', 'CPUTEMP', 'DISK']:
    logg.debug(f'Logging {sensor_name}...')
    sensor = Sensor(sensor_name)
    # Take readings & log to db
    sensor.measure_and_log_to_db(tbl=InfluxDBHomeAuto().__getattribute__(sensor_name), n_times=2)

logg.debug('Temp logging successfully completed.')

logg.close()
