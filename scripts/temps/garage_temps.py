#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read temperature and humidity from living room"""
from pitools import Sensor
from kavalkilu import Log


logg = Log('garage_temp', log_dir='weather', log_to_db=True)
sn = '28-0000079ab34b'
sensor = Sensor('DALLAS', serial=sn)
# Take readings & log to db
sensor.log_to_db()

logg.debug('Temp logging successfully completed.')

logg.close()
