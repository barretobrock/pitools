
class GPIOUnit:
    device_type = 'GPIO'

    def __init__(self, pin: int):
        self.pin = pin


class RelayUnit(GPIOUnit):
    device_type = 'RELAY'

    def __init__(self, pin: int):
        super().__init__(pin)


class DHTUnit(GPIOUnit):
    device_type = 'DHT'

    def __init__(self, pin: int):
        super().__init__(pin)


class DallasUnit:
    device_type = 'DALLAS'

    def __init__(self, name: str, sn: str):
        self.name = name
        self.sn = sn


class UltrasonicUnit:
    device_type = 'ULTRASONIC'

    def __init__(self, trigger_pin: int, echo_pin: int):
        self.trigger = trigger_pin
        self.echo = echo_pin


class PiElutuba:
    dht = DHTUnit(4)


class PiGarage:
    dallas = DallasUnit('garage', '28-0000079ab34b')
    relay = RelayUnit(2)
    ultrasonic = UltrasonicUnit(3, 4)
    ha_garage_door_sensor = 'binary_sensor.garage_door'