#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detects whether the garage door is up or down"""
from kavalkilu import LogWithInflux, HAHelper
from pitools import DistanceSensor
from pitools.peripherals import PiGarage


logg = LogWithInflux('garage_door', log_dir='gdoor')


TRIGGER_PIN = PiGarage.ultrasonic.trigger
ECHO_PIN = PiGarage.ultrasonic.echo
logg.debug('Initializing sensor...')
ds = DistanceSensor(TRIGGER_PIN, ECHO_PIN)

# Take an average of 10 readings
readings = []
logg.debug('Taking readings...')
for i in range(10):
    readings.append(ds.measure())

avg = sum(readings) / len(readings)

# Instantiate HASS
ha = HAHelper()
# Collect last reading
last_status = ha.get_state(PiGarage.ha_garage_door_sensor).get('state')

# Typically, reading is ca. 259cm when door is closed. ca. 50cm when open
if avg < 6000:
    status = 'open'
    # TODO: Depth when car is in
else:
    status = 'closed'
logg.debug(f'Door is {status}. Reading of {avg}')
if last_status != status:
    ha.set_state(PiGarage.ha_garage_door_sensor, {'state': status})

logg.close()
