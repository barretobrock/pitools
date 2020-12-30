#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read temperature and humidity from living room"""
from kavalkilu import LogWithInflux
from pitools import Sensor
from pitools.peripherals import PiElutuba


logg = LogWithInflux('elutuba_temp', log_dir='weather')

# Set the pin (BCM)
sensor = Sensor('DHT22', data_pin=PiElutuba.dht.pin)
# Take readings & log to db
sensor.log_to_db()

logg.debug('Temp logging successfully completed.')

logg.close()
