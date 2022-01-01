'''
sudo pip3 install adafruit-circuitpython-ads1x15

'''
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format("raw", "v"))

while True:
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(0.5)

'''
class Acp:
    def __init__(self):
        
        #Класс описывающий взаимодействие и опрос датчиков тока 
        
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads13 = ADS.ADS1115(self.i2c)
        self.adc46 = ADS.ADS1115(self.i2c, address=0x49)

        a1 = AnalogIn(self.ads13, ADS.P0)
        a2 = AnalogIn(self.ads13, ADS.P1)
        a3 = AnalogIn(self.ads13, ADS.P2)
        a4 = AnalogIn(self.adc46, ADS.P0)
        a5 = AnalogIn(self.adc46, ADS.P1)
        a6 = AnalogIn(self.adc46, ADS.P2)

        self.CorNulA1 = a1.value
        self.CorNulA2 = a2.value
        self.CorNulA3 = a3.value
        self.CorNulA4 = a4.value
        self.CorNulA5 = a5.value
        self.CorNulA6 = a6.value

    def ReadAmperemeter(self, MassOut: dict):
        
        #Функция опроса датчиков тока 
        
        a1 = AnalogIn(self.ads13, ADS.P0)
        a2 = AnalogIn(self.ads13, ADS.P1)
        a3 = AnalogIn(self.ads13, ADS.P2)
        a4 = AnalogIn(self.adc46, ADS.P0)
        a5 = AnalogIn(self.adc46, ADS.P1)
        a6 = AnalogIn(self.adc46, ADS.P2)
        # Потенциально кривой матан
        MassOut['a1'] = round((a1.value - self.CorNulA1) * 0.00057321919, 3)
        MassOut['a2'] = round((a2.value - self.CorNulA2) * 0.00057321919, 3)
        MassOut['a3'] = round((a3.value - self.CorNulA3) * 0.00057321919, 3)
        MassOut['a4'] = round((a4.value - self.CorNulA4) * 0.00057321919, 3)
        MassOut['a5'] = round((a5.value - self.CorNulA5) * 0.00057321919, 3)
        MassOut['a6'] = round((a6.value - self.CorNulA6) * 0.00057321919, 3)

        return MassOut
'''

'''
Протестированно работает, надо подлючить анемометр и попробовать имерять скороть ветра, так же надо реализовать перевод из вольтажа а скорость ветра.
'''