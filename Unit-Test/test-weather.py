import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import smbus2
import bme280
#import adafruit_bh1750 
import FaBo9Axis_MPU9250                         
import time
import board
import busio
import sys

time.sleep(1)

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)
       
i2c = board.I2C()
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)

#lux_sensor = adafruit_bh1750.BH1750(i2c)
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

while 1:
    
    mag = mpu9250.readMagnet()

    print ('{}'.format('-'*30))

    print ('Temp      = {0:0.3f} deg C'.format(data.temperature))
    print ('Pressure  = {0:0.2f} hPa'.format(data.pressure))
    print ('Humidity  = {0:0.2f} %'.format(data.humidity))
   # print ('Bright    = {0:0.2f} lux'.format(light))
    print ('Mag       x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f} uT'.format(mag['x'],mag['y'],mag['z']))
    print ('Anem      = {:>5}\t Voltage = {:>5.3f}'.format(chan.value, chan.voltage))
    
    print ('{}'.format('-'*30))
    
    time.sleep(5)
