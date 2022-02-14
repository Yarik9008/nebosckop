# импорт конфиг настроек
from config import utelegram_config
from config import wifi_config
# импорт библиотек для работы с bme280
from machine import Pin, I2C
from time import sleep
import BME280
# импорт библиотек для телеграмм бота
import telegram2
import network
import utime

debug = True

#  подключение к точке доступа
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect(wifi_config['ssid'], wifi_config['password'])

# подключение к датчику
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)

# задержка для подключения к сути wifi
if debug:
    print('WAITING FOR NETWORK - sleep 20')
utime.sleep(20)

# функция опроса датчика bme280
def reqiest_weather(message):
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure * 0.750062

    bot.send(message['message']['chat']['id'],
             f'Weather realtime:\nTerm = {temp} С\nPressure = {pres} mm\nHumidity = {hum} %')

# инициализация телеграм бота 
if sta_if.isconnected():
    bot = telegram2.ubot(utelegram_config['token'])
    bot.register('/weather', reqiest_weather)

    print('BOT LISTENING')
    bot.listen_blocking()
else:
    print('NOT CONNECTED - aborting')


# список доступных комманд 
'''
weather - get real time weather

'''