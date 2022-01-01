'''
sudo pip3 install adafruit-circuitpython-bh1750
'''

import time
import board
import adafruit_bh1750

class NeboscopeBH1750:
    def __init__(self):
        i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(i2c)

    def interview(self):
        return {'lux': self.sensor.lux}


if __name__ == '__main__':
    testbh170 = NeboscopeBH1750()
    print(testbh170.interview())

'''
Не подключен 
'''