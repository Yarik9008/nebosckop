import telebot
from config import *
from NeboscopeUnitHardware import *
import cv2

'''
погода-получение погоды в реальном времени
фото-получение фото в реальном времени
неостарт-включение теста адресной ленты
неостоп-выключить адресную ленту

weather - get real time weather
photo - get real time photo
neostart - turn on the address tape 
neostop - turn off the address tape

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
# 
try:
    neo = NeboscopeNeopix()
    logger.info('init neopix')
    neo.start_init_neo()
except:
    logger.warning('no init neopix')


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
    temp, pressure, humidity, lyx = massdata['temp'], massdata['pressure'], massdata['humidity'], massdata['lux']
    bot.send_message(message.chat.id, f'Weather realtime:\nTerm = {temp}\nPressure = {pressure}\nHumidity = {humidity}\nLyx = {lyx}')
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

# Комманда '/neostart'
@bot.message_handler(commands=['neostart'])
def neo_start(message):
    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, 'Neboscope neo start')
    neo.check = True
    neo.start_init_neo()
    bot.send_message(message.chat.id, 'Neboscope neo finish')

# Комманда '/neostop'
@bot.message_handler(commands=['neostop'])
def neo_start(message):
    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, 'Neboscope neo finish')
    neo.stop_swow()

# Комманда '/neostop'
@bot.message_handler(commands=['neostart-rotat'])
def neo_start(message):
    logger.debug(f'User: {message.from_user.username} Data: {message.text}')
    bot.send_message(message.chat.id, 'Neboscope neo finish')
    neo.stop_swow()

bot.infinity_polling()