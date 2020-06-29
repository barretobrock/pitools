#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read temperatures from several locations outside using Dallas sensors"""
from time import sleep
from kavalkilu import Log
from pitools import Sensor


logg = Log('porch_temp', log_dir='weather', log_to_db=True)
# Serial numbers of the Dallas temp sensors
sensors = [
    {
        'sn': '28-0316b5f72bff',
        'loc': 'porch_upper_shade',
    }, {
        'sn': '28-0516a4a84eff',
        'loc': 'porch_upper_sun',
    }, {
        'sn': '28-0416c17b86ff',
        'loc': 'porch_lower_shade',
    }
]

for sensor_dict in sensors:
    logg.debug(f'Collecting info for {sensor_dict["loc"]}')
    sensor = Sensor('DALLAS', serial=sensor_dict['sn'], loc_override=sensor_dict['loc'])
    sensor.log_to_db(2)
    sleep(1)

logg.debug('Temp logging successfully completed.')

logg.close()
