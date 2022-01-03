from time import sleep
import telebot
import config
import logging
#import coloredlogs
from datetime import datetime
from pprint import pprint
from NeboscopeUnitHardware import *


class Neboscope_Logging:
    '''Класс отвечающий за логирование. Логи пишуться в файл, так же выводться в консоль'''

    def __init__(self):
        self.mylogs = logging.getLogger(__name__)
        self.mylogs.setLevel(logging.DEBUG)
        # обработчик записи в лог-файл
        name = 'log/' + \
            '-'.join('-'.join('-'.join(str(datetime.now()).split()
                                       ).split('.')).split(':')) + 'log'
        self.file = logging.FileHandler(name)
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


class NeboscopeTelBot:
    def __init__(self, token):
        self.weather_name_mass = ['weather', 'погода']
        self.logger = Neboscope_Logging()
        try:
            self.bot = telebot.TeleBot(token)
            self.bot.set_update_listener(self.input_massage)
            self.logger.info('init telegram bot')
        except:
            self.logger.warning('no init telegram bot')

        try:
            self.lyx_metr = NeboscopeBH1750()
            self.logger.info('init lyx-metr')
        except:
            self.logger.warning('no init lyx-metr')

        try:
            self.term_h_p = NeboscopeBME280()
            self.logger.info('init bme280')
        except:
            self.logger.warning('no init bme280')

    def input_massage(self, message):
        for mes in message:
            print(str(mes))
            if mes.content_type == 'text' and mes.text in self.weather_name_mass:
                self.request_weather(mes)
            elif mes.content_type == 'text' and len(mes.text.lower().split()) == 2:
                self.request_stek_weather(mes)
            elif mes.content_type == 'text' and len(mes.text.lower().split()) == 4 and mes.text.lower().split()[0] == 'запись':
                self.write_weather_file(mes)
            else:
                self.bot.send_message(mes.chat.id, 'No command: ' + mes.text)

    def request_weather(self, message):
        name = message.from_user.username
        massdata = {**self.lyx_metr.reqiest(), **self.term_h_p.reqiest()}
        temp, pressure, humidity = massdata['temp'], massdata['pressure'], massdata['humidity']
        self.bot.send_message(
            message.chat.id, f'Weather realtime:\nTerm = {temp}\nPressure = {pressure}\nHumidity = {humidity}\nGoodbye {name}!')

    def request_stek_weather(self, message):
        tip = message.text.lower().split()[0]
        n = message.text.lower().split()[1]
        name = message.from_user.username
        if tip == 'температура':
            for i in range(int(n)):
                massdata = self.term_h_p.reqiest()
                temp, pressure, humidity = massdata['temp'], massdata['pressure'], massdata['humidity']
                self.bot.send_message(message.chat.id, f'Temp: {temp} C')
                sleep(0.5)
        elif tip == 'влажность':
            for i in range(int(n)):
                massdata = self.term_h_p.reqiest()
                temp, pressure, humidity = massdata['temp'], massdata['pressure'], massdata['humidity']
                self.bot.send_message(
                    message.chat.id, f'Humidity: {humidity} %')
                sleep(0.5)
        elif tip == 'давление':
            for i in range(int(n)):
                massdata = self.term_h_p.reqiest()
                temp, pressure, humidity = massdata['temp'], massdata['pressure'], massdata['humidity']
                self.bot.send_message(message.chat.id, f'Давление: {pressure}')
                sleep(0.5)
        elif tip == 'погода':
            for i in range(int(n)):
                massdata = self.term_h_p.reqiest()
                temp, pressure, humidity = massdata['temp'], massdata['pressure'], massdata['humidity']
                self.bot.send_message(
                    message.chat.id, f'Weather realtime:\nTerm = {temp}\nPressure = {pressure}\nHumidity = {humidity}')
                sleep(1)
        else:
            self.bot.send_message(
                message.chat.id, f'no command: {message.text}')

    def write_weather_file(self, message):
        if message.text.lower().split()[1].isalpha() and message.text.lower().split()[2].isdigit() and message.text.lower().split()[3].isdigit():
            tip = message.text.lower().split()[1]
            n = message.text.lower().split()[2]
            timestepp = float(message.text.lower().split()[3])
        else:
            self.bot.send_message(message.chat.id, f'no command: {message.text}')
            return None
            
        name = message.from_user.username
        time = str(datetime.now())
        self.bot.send_message(message.chat.id, f'Writing file {tip} to: {name}_{tip}_{n}_{time}.txt')
        with open(f"file/{name}_{tip}_{n}_{time}.txt", "w") as file1:
            file1.write(f'Settings: Type: {tip} Len: {n} Timesleep: {timestepp} Start-time: {time}\n')
            file1.write(f'Num Temp Pres Hum\n')
            for i in range(int(n)):
                massdata = self.term_h_p.reqiest()
                temp, pressure, humidity = massdata['temp'], massdata['pressure'], massdata['humidity']
                file1.write(f'{i} {temp} {pressure} {humidity}')
                sleep(timestepp)
            self.bot.send_document(file1)

    def main(self):
        self.bot.polling(non_stop=True)


a = NeboscopeTelBot(config.token)
a.main()
