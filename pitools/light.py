#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .gpio import GPIO
import time


class LED:
    """LED light functions"""
    def __init__(self, pin: int):
        """
        Args:
            pin: int, BCM pin to relay
        """
        self.led_pin = GPIO(pin, mode='bcm', status='output')

    def turn_on(self):
        """Turn LED ON"""
        self.led_pin.set_output(1)

    def turn_off(self):
        """Turn LED OFF"""
        self.led_pin.set_output(0)

    def blink(self, times: int, wait: int = 0.1):
        """Blinks LED x times, waiting y seconds between"""
        for x in range(0, times):
            self.turn_on()
            time.sleep(wait / 2)
            self.turn_off()
            time.sleep(wait / 2)
