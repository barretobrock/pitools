#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import psutil
import Adafruit_DHT as dht
from typing import Union, Optional
from kavalkilu import InfluxDBLocal, InfluxDBNames, InfluxTblNames, NetTools
from .gpio import GPIO


class Sensor:
    """
    Universal sensor collection stuff
    """

    def __init__(self, sensor_model: str, decimals: int = 2, data_pin: int = None, serial: str = None):
        """
        :param sensor_model:
        :param decimals:
        :param data_pin:
        :param serial:
        """
        self.decimals = decimals
        # Determine the sensor to use
        sensor_model = sensor_model.upper()
        if sensor_model == 'DHT22':
            # Need data pin
            if data_pin is None:
                raise ValueError('Data pin required for DHT22 sensor.')
            self.sensor = DHTTempSensor(data_pin)
        elif sensor_model == 'DALLAS':
            # Need data pin
            if serial is None:
                raise ValueError('Serial required for DALLAS sensor.')
            self.sensor = DallasTempSensor(serial)
        elif sensor_model == 'CPUTEMP':
            self.sensor = CPUTempSensor()
        elif sensor_model == 'CPU':
            self.sensor = CPUSensor()
        elif sensor_model == 'MEM':
            self.sensor = MEMSensor()
        elif sensor_model == 'DISK':
            self.sensor = DiskSensor()
        else:
            raise ValueError(f'Invalid sensor model selected: {sensor_model}.')

    def round_reads(self, data: Union[int, float, dict]) -> Union[float, dict]:
        """
        Goes through data and rounds info to x decimal places
        Args:
            data: dict, temp/humidity data to round
                keys - 'humidity', 'temp'
        """
        def rounder(value: Union[int, float]) -> float:
            """Rounds the value"""
            if isinstance(value, int):
                value = float(value)
            if isinstance(value, float):
                value = round(value, self.decimals)
            return value

        # Loop through readings, remove any float issues by rounding off to 2 decimals
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = rounder(v)
        elif isinstance(data, (int, float)):
            data = rounder(data)
        return data

    def measure(self, n_times: int = 1, sleep_between_secs: int = 1) -> Optional[dict]:
        """Takes a measurement of the sensor n times"""
        measurements = {}
        for i in range(0, n_times):
            for k, v in self.sensor.take_reading().items():
                if k in measurements.keys():
                    measurements[k].append(v)
                else:
                    measurements[k] = [v]
            time.sleep(sleep_between_secs)

        # Take average of the measurements
        for key, val in measurements.items():
            if len(val) > 0:
                # Calculate the average
                measurements[key] = sum(val) / len(val)
            else:
                # Take out the measurement
                _ = measurements.pop(key)

        return self.round_reads(measurements)

    def log_to_db(self, n_times: int = 5, sleep_between_secs: int = 1, tbl: str = InfluxTblNames.TEMPS):
        """Logs the measurements to Influx"""
        # Take measurements
        measurements = self.measure(n_times, sleep_between_secs)
        if measurements is None:
            raise ValueError('Unable to log data: measurement was NoneType.')
        if len(measurements) == 0:
            raise ValueError('Unable to log data: measurement dict was empty.')
        tags = {
            'location': NetTools().hostname
        }
        # Connect to db and load data
        influx = InfluxDBLocal(InfluxDBNames.HOMEAUTO)
        influx.write_single_data(tbl=tbl, tag_dict=tags, field_dict=measurements)
        # Close database
        influx.close()


class DHTTempSensor:
    """
    DHT Temperature sensor
    """
    def __init__(self, pin: int):
        """
        Args:
            pin: int, BCM pin number for data pin to DHT sensor
        """
        self.sensor_model = 'DHT22'
        self.sensor = dht.DHT22
        self.pin = pin

    @staticmethod
    def _check_is_none(*args) -> bool:
        """Checks if any items in the list are None"""
        return any([x is None for x in args])

    def take_reading(self) -> dict:
        """Attempts to read in the sensor data"""
        humidity, temp = dht.read_retry(self.sensor, self.pin)
        if not self._check_is_none(humidity, temp):
            return {
                'temp': temp,
                'humidity': humidity
            }
        return {}


class DallasTempSensor:
    """
    Dallas-type temperature sensor
    """
    def __init__(self, serial: str):
        """
        Args:
            serial: str, the serial number for the temperature sensor.
                NOTE: found in /sys/bus/w1/devices/{}/w1_slave
        """
        self.sensor_model = 'DALLAS'
        self.sensor_path = f'/sys/bus/w1/devices/{serial}/w1_slave'

    def take_reading(self) -> dict:
        """Attempts to read in the sensor data"""
        with open(self.sensor_path) as f:
            result = f.read()
        result_list = result.split('\n')
        temp = None
        for r in result_list:
            # Loop through line breaks and find temp line
            if 't=' in r:
                temp = float(r[r.index('t=') + 2:]) / 1000
                break
        if temp is not None:
            return {'temp': temp}
        return {}


class CPUTempSensor:
    """
    CPU temperature sensor
    """

    def __init__(self):
        self.sensor_model = 'CPU'
        self.cpu_temp = psutil.sensors_temperatures

    def take_reading(self) -> dict:
        """Attempts to read in the sensor data"""
        return {'cpu-temp': self.cpu_temp()['cpu-thermal'][0].current}


class CPUSensor:
    """
    CPU use sensor
    """

    def __init__(self):
        self.sensor_model = 'CPU'
        self.cpu = psutil.cpu_percent

    def take_reading(self) -> dict:
        """Attempts to read in the sensor data"""
        return {'cpu-use': self.cpu()}


class MEMSensor:
    """
    Memory use sensor
    """

    def __init__(self):
        self.sensor_model = 'MEM'
        self.ram = psutil.virtual_memory()

    def take_reading(self) -> dict:
        """Attempts to read in the sensor data"""
        # Collect memory usage data
        mem_data = {
            'ram-total': self.ram.total / 2 ** 20,
            'ram-used': self.ram.used / 2 ** 20,
            'ram-free': self.ram.free / 2 ** 20,
            'ram-percent_used': self.ram.percent / 100
        }

        return mem_data


class DiskSensor:
    def __init__(self):
        self.sensor_model = 'DISK'
        self.disk = psutil.disk_usage('/')

    def take_reading(self) -> dict:
        """Attempts to read in the sensor data"""
        # Collect disk usage data
        disk_data = {
            'disk-total': self.disk.total / 2 ** 30,
            'disk-used': self.disk.used / 2 ** 30,
            'disk-free': self.disk.free / 2 ** 30,
            'disk-percent_used': self.disk.percent / 100
        }

        return disk_data


class PIRSensor:
    """
    Functions for a PIR motion sensor
    """
    def __init__(self, pin: int):
        """
        Args:
            pin: int, the BCM pin related to the PIR sensor
        """
        self.sensor = GPIO(pin, mode='bcm', status='input')
        self.sensor_type = 'PIR'

    def arm(self, sleep_sec: float = 0.1, duration_sec: int = 300) -> Optional[float]:
        """
        Primes the sensor for detecting motion.
            If motion detected, returns unix time
        Args:
            sleep_sec: float, seconds to sleep between checks
            duration_sec: int, seconds to run script before exit
        """
        # Get current time
        start_time = time.time()
        end_time = start_time + duration_sec

        while end_time > time.time():
            # Measure once
            m1 = self.sensor.get_input()
            # Pause
            time.sleep(sleep_sec)
            # Measure twice
            m2 = self.sensor.get_input()
            if all([m1 == 1, m2 == 1]):
                return time.time()
        return None


class DistanceSensor:
    """Functions for the HC-SR04 Ultrasonic range sensor"""
    def __init__(self, trigger_pin: int, echo_pin: int):
        self.sensor_type = 'ULTRASONIC'
        self.sensor_model = 'HC-SR04'
        # Set up the trigger
        self.trigger = GPIO(trigger_pin, status='output')
        # Set up feedback
        self.echo = GPIO(echo_pin, status='input')

    def measure(self, wait_time: int = 2, pulse_time: float = 0.00001, round_decs: int = 2) -> float:
        """Take distance measurement in mm"""
        # Wait for sensor to settle
        self.trigger.set_output(0)
        time.sleep(wait_time)
        # Pulse trigger
        self.trigger.set_output(1)
        time.sleep(pulse_time)
        self.trigger.set_output(0)

        # Get feedback
        pulse_start = pulse_end = None
        while self.echo.get_input() == 0:
            pulse_start = time.time()

        while self.echo.get_input() == 1:
            pulse_end = time.time()

        if not all([x is not None for x in [pulse_start, pulse_end]]):
            raise ValueError('Pulse start/stops not detected.')

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150 * 100
        distance = round(distance, round_decs)

        return distance

    def close(self):
        """Clean up the pins associated with the sensor"""
        self.echo.cleanup()
        self.trigger.cleanup()

    def __del__(self):
        """Cleanup on deletion"""
        self.close()
