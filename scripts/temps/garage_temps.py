#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read temperature and humidity from living room"""
from kavalkilu import LogWithInflux
from pitools import Sensor
from pitools.peripherals import PiGarage


logg = LogWithInflux('garage_temp', log_dir='weather')

sensor = Sensor('DALLAS', serial=PiGarage.dallas.sn)
# Take readings & log to db
sensor.measure_and_log_to_db(send_to_ha=True)

logg.debug('Temp logging successfully completed.')

logg.close()
