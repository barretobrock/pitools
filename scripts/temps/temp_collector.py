#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read temperature and humidity from living room"""
import json
from pitools import Sensor
from kavalkilu import LogWithInflux, Path, NetTools


logg = LogWithInflux('elutuba_temp', log_dir='weather')
p = Path('pi')
peripherals_path = p.easy_joiner(p.extras_dir, ['pitools', 'scripts', 'peripherals.json'])

# Read in the peripherals file
with open(peripherals_path) as f:
    pers = json.loads(f.read())

# machine_name = 'pi-elutuba'
machine_name = NetTools().hostname

for k, v in pers.items():
    sensor = None
    name_split = k.split('-')
    if len(name_split) > 1:
        name = '-'.join(name_split[1:])
    else:
        name = machine_name

    if k.startswith('dht'):
        # DHT22 sensor
        sensor = Sensor('DHT22', data_pin=v, loc_override=name)
    elif k.startswith('dallas'):
        # DALLAS sensor
        sensor = Sensor('DALLAS', serial=v, loc_override=name)

    if sensor is not None:
        # Take readings & log to db
        sensor.log_to_db()
        logg.debug('Temp logging successfully completed.')

logg.close()
