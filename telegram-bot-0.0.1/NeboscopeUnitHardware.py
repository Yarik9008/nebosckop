import smbus2
import bme280
import board
import adafruit_bh1750


class NeboscopeBH1750:
    def __init__(self):
        i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(i2c)

    def reqiest(self):
        return {'lux': self.sensor.lux}


class NeboscopeBME280:
    def __init__(self, port=1, address=0x7):
        self.port = 1
        self.address = 0x76
        self.bus = smbus2.SMBus(port)
        self.calibration_params = bme280.load_calibration_params(
            self.bus, self.address)

    def reqiest(self):
        self.data = bme280.sample(
            self.bus, self.address, self.calibration_params)
        return {'temp': self.data.temperature,
               'pressure': self.data.pressure,
               'humidity': self.data.humidity}