'''
 sudo pip3 install RPi.bme280

'''
import smbus2
import bme280

class NeboscopeBME280:
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

if __name__ == '__main__':
    testbme280 = NeboscopeBME280()
    print(testbme280.interview())
    
    
'''
Протестированно работает штатно.
'''