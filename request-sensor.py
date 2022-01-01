
import struct
import board
import busio
import smbus2
import bme280
import serial
import pynmea2
import neopixel
import FaBo9Axis_MPU9250
import adafruit_bh1750
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep



class NeboscopeBME280:
    # опрос датчика температуры 
    def __init__(self, port=1, address=0x7):
        self.port = 1
        self.address = 0x76
        self.bus = smbus2.SMBus(port)
        self.calibration_params = bme280.load_calibration_params(
            self.bus, self.address)

    def interview(self):
        self.data = bme280.sample(
            self.bus, self.address, self.calibration_params)
        return {'temp': self.data.temperature,
                'pressure': self.data.pressure,
                'humidity': self.data.humidity}


class NeboscopeBH1750:
    # опрос датчика освещенности
    def __init__(self):
        i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(i2c)

    def interview(self):
        return {'lux': self.sensor.lux}


class NeboscopeADS1115:
    # опрос ацп (аналогово-цифрового-преобразователя) 
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        self.chan = AnalogIn(ads, ADS.P0)

    def interview(self):
        return {'wind': round(self.chan.value * 5, 1)}


class NeboscopeMpu9250:
    # опрос датчика ориентации
    def __init__(self):
        self.mpu9250 = FaBo9Axis_MPU9250.MPU9250()

    def interview(self):
        accel = self.mpu9250.readAccel()
        gyro = self.mpu9250.readGyro()
        mag = self.mpu9250.readMagnet()

        return{'ax': accel['x'], 'ay': accel['y'], 'az': accel['z'],
               'gx': gyro['x'], 'gy': gyro['y'], 'gz': gyro['z'],
               'mx': mag['x'], 'my': mag['y'], 'mz': mag['z']}


class NeboscopeGPS:
    # опрос GPS датчика (пока в стадии допиливания но для общего понимания данные он выводит так)
    def __init__(self):
        pass

    def interview(self):
        return{'lat': 0, 'long': 0}


class NeboscopeSensor:
    # класс-адаптер 
    def __init__(self):
        self.bme280 = NeboscopeBME280()
        self.bh1750 = NeboscopeBH1750()
        self.ads1115 = NeboscopeADS1115()
        self.mpu9250 = NeboscopeMpu9250
        self.gps = NeboscopeGPS()

    def interview(self):
        return {**self.bme280.interview(), **self.bh1750.interview(), **self.ads1115.interview(), **self.mpu9250.interview(), **self.gps.interview()}

if __name__ == '__main__':
    neb = NeboscopeSensor()
    while True:
        print(neb.interview())
        sleep(0.5)
