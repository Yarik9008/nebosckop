import serial
from time import sleep
from datetime import datetime
from ast import While, literal_eval
'''
Примеры команд:
$homing;
$rotation 180 90;

$ - стартовый символ
; - конечный символ
homing - команда для позиционирования в ноль
rotation - команда для поворота на угол. Первый параметр - угол наклона, второй - угол поворота
при запуске одной из функций в СОМ-порт отправляется сообщение OK

'''

DEBUG = False


class PULT_Logging:
    def __init__(self) -> None:
        pass

    def critical(*args):
        pass

    def debug(*args):
        pass

    def warning(*args):
        pass


class Rotator_SerialPort:
    def __init__(self,
                 logger: PULT_Logging = PULT_Logging,
                 port: str = '/dev/ttyAMA0',
                 bitrate: int = 9600
                 ):
        global DEBUG
        # инициализация переменных
        self.check_connect = False
        self.logger = logger
        # открытие порта 
        self.serial_port = serial.Serial(
            port=port,
            baudrate=bitrate,
            timeout=0.1)

    def Receiver_tnpa(self):
        global DEBUG
        '''прием информации с аппарата'''
        data = None

        while data == None or data == b'':
            data = self.serial_port.readline()

        try:
            dataout = list(map(lambda x: float(x), str(data)[3:-4].split(', ')))
        except:
            self.logger.warning('Error converting data')
            return None

        if DEBUG:
            self.logger.debug(f'Receiver data : {str(data)}')
        return dataout

    def homing(self):
        global DEBUG
        '''отправка массива на аппарат'''
        self.serial_port.write('$homing;\n'.encode())
        if DEBUG:
            self.logger.debug('Send data: ' + '$homing;')

test_log = PULT_Logging()
test_pult = Rotator_SerialPort()

if __name__ == '__main__':
    while True:
        a = input()
        test_pult.homing()