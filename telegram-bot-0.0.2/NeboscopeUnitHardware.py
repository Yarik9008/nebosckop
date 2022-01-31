import smbus2
import bme280
import board
import adafruit_bh1750
import time
import neopixel
import logging
from datetime import datetime

class NeboscopeBH1750:
    def __init__(self):
        i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(i2c)

    def reqiest(self):
        try:
            return {'lux': round(self.sensor.lux, 2)}
        except:
            return{'lux': None}


class NeboscopeBME280:
    def __init__(self, port=1, address=0x7):
        self.port = 1
        self.address = 0x76
        self.bus = smbus2.SMBus(port)
        self.calibration_params = bme280.load_calibration_params(
            self.bus, self.address)

    def reqiest(self):
        try:
            self.data = bme280.sample(
                self.bus, self.address, self.calibration_params)
            return {'temp': round(self.data.temperature, 2),
                    'pressure': round(self.data.pressure, 2),
                    'humidity': round(self.data.humidity, 2)}
        except:
            return {'temp': None,
                    'pressure': None,
                    'humidity': None}


class NeboscopeNeopix:
    def __init__(self) -> None:
        self.pixel_pin = board.D18
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, 64, brightness=1, auto_write=False, pixel_order=self.ORDER)
        self.check = True
    
    def starting_func(self, color, delay):
        for i in range(16):
            if not self.check and not color == (0,0,0):
                break
            self.pixels[i] = color
            self.pixels[31 - i] = color
            self.pixels[i + 31] = color
            self.pixels[63 - i] = color
            self.pixels.show()
            time.sleep(delay)
        
    
    def start_init_neo(self):
        self.starting_func((255, 0, 0), 0.2)
        self.starting_func((0, 255, 0), 0.2)
        self.starting_func((0, 0, 255), 0.2)
        self.starting_func((0, 0, 0), 0)

    
    
    def start_swow(self, wait=0.0001):
        def wheel(pos):
            if pos < 0 or pos > 255:
                r = g = b = 0
            elif pos < 85:
                r = int(pos * 3)
                g = int(255 - pos * 3)
                b = 0
            elif pos < 170:
                pos -= 85
                r = int(255 - pos * 3)
                g = 0
                b = int(pos * 3)
            else:
                pos -= 170
                r = 0
                g = int(pos * 3)
                b = int(255 - pos * 3)
            return (r, g, b)



        while self.check:
            for j in range(255):
                for i in range(16):
                    if not self.check:
                        break
                    pixel_index = (i * 256 // 16) + j
                    self.pixels[i] = wheel(pixel_index & 255)
                    self.pixels[31 - i] = wheel(pixel_index & 255)
                    self.pixels[i + 31] = wheel(pixel_index & 255)
                    self.pixels[63 - i] = wheel(pixel_index & 255)
                    self.pixels.show()
                time.sleep(wait)
                if not self.check:
                    break

    def stop_swow(self):
        self.check = False
        self.starting_func((0, 0, 0), 0)


class Neboscope_Logging:
    '''Класс отвечающий за логирование. Логи пишуться в файл, так же выводться в консоль'''

    def __init__(self):
        self.mylogs = logging.getLogger(__name__)
        self.mylogs.setLevel(logging.DEBUG)
        # обработчик записи в лог-файл
        self.name = 'log/' + \
            '-'.join('-'.join('-'.join(str(datetime.now()).split()
                                       ).split('.')).split(':')) + 'log'
        self.file = logging.FileHandler(self.name)
        self.fileformat = logging.Formatter(
            "%(asctime)s:%(levelname)s:%(message)s")
        self.file.setLevel(logging.DEBUG)
        self.file.setFormatter(self.fileformat)
        # обработчик вывода в консоль лог файла
        self.stream = logging.StreamHandler()
        self.streamformat = logging.Formatter(
            "%(levelname)s:%(module)s:%(message)s")
        self.stream.setLevel(logging.DEBUG)
        self.stream.setFormatter(self.streamformat)
        # инициализация обработчиков
        self.mylogs.addHandler(self.file)
        self.mylogs.addHandler(self.stream)
        #coloredlogs.install(level=logging.DEBUG, logger=self.mylogs, fmt='%(asctime)s [%(levelname)s] - %(message)s')

        self.mylogs.info('start-logging-sistem')

    def debug(self, message):
        '''сообщения отладочного уровня'''
        self.mylogs.debug(message)

    def info(self, message):
        '''сообщения информационного уровня'''
        self.mylogs.info(message)

    def warning(self, message):
        '''не критичные ошибки'''
        self.mylogs.warning(message)

    def critical(self, message):
        self.mylogs.critical(message)

    def error(self, message):
        self.mylogs.error(message)
