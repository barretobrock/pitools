#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read temperature and humidity from living room"""
from pitools import DHTTempSensor as DHT
from kavalkilu import Log


log = Log('elutuba_temp', log_dir='weather')
# Set the pin
TEMP_PIN = 4
sl = SensorLogger('living_room', DHT(TEMP_PIN, decimals=3))
# Take in readings, update openhab & mysql data sources
sl.update()

log.debug('Temp logging successfully completed.')

log.close()
