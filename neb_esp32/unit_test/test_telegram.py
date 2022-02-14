
from config import utelegram_config
from config import wifi_config

import telegram2
import network
import utime

debug = True

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect(wifi_config['ssid'], wifi_config['password'])

if debug: print('WAITING FOR NETWORK - sleep 20')
utime.sleep(20)

def get_message(message):
    bot.send(message['message']['chat']['id'], message['message']['text'].upper())

def reply_ping(message):
    print(message)
    bot.send(message['message']['chat']['id'], 'pong')
    
def hello(message):
    bot.send(message['message']['chat']['id'], 'hello')

if sta_if.isconnected():
    bot = telegram2.ubot(utelegram_config['token'])
    bot.register('/ping', reply_ping)
    bot.register('/hello', hello)
    bot.set_default_handler(get_message)

    print('BOT LISTENING')
    bot.listen_blocking()
else:
    print('NOT CONNECTED - aborting')
