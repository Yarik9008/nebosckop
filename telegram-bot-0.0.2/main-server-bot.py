import telebot
import cv2
from config import *
from orbital import *
from NeboscopeUnitHardware import *
from NeboscopeLedStrip import *


'''
погода-получение погоды в реальном времени
фото-получение фото в реальном времени
неостарт-включение теста адресной ленты
неостоп-выключить адресную ленту
weather - Get real time weather
photo - Get real time photo
scheduleapt - Request schedule apt 
scheduleL - Request schedule l
updatetle - Update tle data
neostart1 - Neo_1
neostart2 - Neo_2
neostart3 - Neo_3
neostart4 - Neo_4
neostart5 - Neo_5
neostart6 - Neo_6
neostart7 - Neo_7
neostart8 - Neo_8
neostart9 - Neo_9
neostart10 - Neo_10
neostart11 - Neo_11
neostart12 - Neo_12
neostart13 - Neo_13
neostop - Turn off the address tape
'''

### init ###
# логирование 
logger = Neboscope_Logging()
try:
    bot = telebot.TeleBot(TOKEN)
    logger.info('init telegram bot')
except:
    logger.warning('no init telegram bot')
# датчик освещенности 
try:
    lyx_metr = NeboscopeBH1750()
    logger.info('init lyx-metr')
except:
    logger.warning('no init lyx-metr')
# датчик температуры, давления, влажности 
try:
    term_h_p = NeboscopeBME280()
    logger.info('init bme280')
except:
    logger.warning('no init bme280')
# работа с камерой
try:
    cam = cv2.VideoCapture(0)
    logger.info('init cam')
except:
    logger.warning('no init cam')

# работа с адресной светодиодной лентой 
try:
    #neo = NeboscopeNeopix()
    neo = LedStrip()
    logger.info('init neopix')
    neo.effect(1)
except:
    logger.warning('no init neopix')

# работа с библиотекой для рассчета пролетов 
try:
   # path = 'C:/Users/Yarik9008/YandexDisk/nebosckop/telegram-bot-0.0.2'
    path = '/home/ubuntu/nebosckop/telegram-bot-0.0.2'
    lat, lon, height = 55.3970, 55.3970, 130
    orbital_apt = Lorett_Orbital('lex', lon, lat, height, path, timeZone=3)
    orbital_l = Lorett_Orbital('l2s', lon, lat, height, path, timeZone=3)
    logger.info('init orbital')
except:
    logger.warning('no init orbital')


# Комманда '/start' 
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет :), Меня зовут НебоскопБот.
Чтобы получить список того что я умею испльзуйте комманду /listproject.
""")


# Комманда '/weather'
@bot.message_handler(commands=['weather'])
def send_weather(message):
    
    massdata = {**lyx_metr.reqiest(), **term_h_p.reqiest()}

    temp, pressure, humidity, lux = massdata['temp'], massdata['pressure'], massdata['humidity'], massdata['lux']

    bot.send_message(message.chat.id, f'Weather realtime:\nTerm = {temp}\nPressure = {pressure}\nHumidity = {humidity}\nLyx = {lux}')
    
    logger.debug(f'User: {message.from_user.username} Data: {message.text}')


# Комманда '/photo'
@bot.message_handler(commands=['photo'])
def send_photo(message):

    name = message.from_user.username
    time = str(datetime.now())
    for i in range(20):
        ret, frame = cam.read()
    namefile = f"file/{name}_{time}.png"
    cv2.imwrite(namefile, frame)
    photo = open(namefile,  'rb')
    bot.send_photo(message.chat.id, photo)
    photo.close()
    logger.debug(f'User: {message.from_user.username} Data: {message.text}')


# Комманда '/neostart1'
@bot.message_handler(commands=['neostart1'])
def neo_start(message):

    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, 'Neboscope neo start 1')
    neo.check = True
    neo.effect(1)
    bot.send_message(message.chat.id, 'Neboscope neo finish')

# Комманда '/neostart2'
@bot.message_handler(commands=['neostart2'])
def neo_start(message):

    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, 'Neboscope neo start 2')
    neo.check = True
    neo.effect(2)
    bot.send_message(message.chat.id, 'Neboscope neo finish')

# Комманда '/neostart3'
@bot.message_handler(commands=['neostart3'])
def neo_start(message):

    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, 'Neboscope neo start 3')
    neo.check = True
    neo.effect(3)
    bot.send_message(message.chat.id, 'Neboscope neo finish')

# Комманда '/neostart4'
@bot.message_handler(commands=['neostart4'])
def neo_start(message):

    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, 'Neboscope neo start 4')
    neo.check = True
    neo.effect(4)
    bot.send_message(message.chat.id, 'Neboscope neo finish')

# Комманда '/neostart5'
@bot.message_handler(commands=['neostart5'])
def neo_start(message):

    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, 'Neboscope neo start 5')
    neo.check = True
    neo.effect(5)
    bot.send_message(message.chat.id, 'Neboscope neo finish')


# Комманда '/neostop'
@bot.message_handler(commands=['neostop'])
def neo_start(message):

    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, 'Neboscope neo finish')
    neo.stop()


# # Комманда '/neostop'
# @bot.message_handler(commands=['neostart-rotat'])
# def neo_start(message):

#     logger.debug(f'User: {message.from_user.username} Data: {message.text}')
#     bot.send_message(message.chat.id, 'Neboscope neo finish')
#     neo.stop_swow()


# Комманда '/scheduleApt'
@bot.message_handler(commands=['scheduleapt'])
def neo_start(message):
    
    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, orbital_apt.getSchedule(48, returnTable=True) )


# Комманда '/scheduleL'
@bot.message_handler(commands=['schedulel'])
def neo_start(message):
    
    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, orbital_l.getSchedule(48, returnTable=True))


# Комманда '/updateTle'
@bot.message_handler(commands=['updatetle'])
def neo_start(message):
    
    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    check = orbital_l.update_tle()
    bot.send_message(message.chat.id, f'Tle update data: {check}' )


bot.infinity_polling()