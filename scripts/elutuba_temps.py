#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read temperature and humidity from living room"""
from pitools import Sensor
from kavalkilu import Log


logg = Log('elutuba_temp', log_dir='weather', log_to_db=True)
# Set the pin (BCM)
PIN = 4
sensor = Sensor('DHT22', data_pin=PIN)
# Take readings & log to db
sensor.log_to_db()

logg.debug('Temp logging successfully completed.')

logg.close()
