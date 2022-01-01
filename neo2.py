# Raspberry or ESP8266

#runtime = 'ESP8266'
runtime = 'Raspberry'

if runtime == 'Raspberry':
    import time
    import board
    import neopixel

    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = board.D18
    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    ORDER = neopixel.GRB
    pixels = neopixel.NeoPixel(
        pixel_pin, 64, brightness=1, auto_write=False, pixel_order=ORDER
    )
elif runtime == 'ESP8266':
    import time
    import machine
    import neopixel

    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = machine.Pin(5, machine.Pin.OUT)
    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    pixels = neopixel.NeoPixel(
        pixel_pin, 64)


def starting_func(color, delay):
    for i in range(16):
        pixels[i] = color
        pixels[31 - i] = color
        pixels[i + 31] = color
        pixels[63 - i] = color
        if runtime == 'Raspberry':
            pixels.show()
        elif runtime == 'ESP8266':
            pixels.write()
        time.sleep(delay)


def fill(color, delay):
    pixels.fill(color)
    if runtime == 'Raspberry':
        pixels.show()
    elif runtime == 'ESP8266':
        pixels.write()
    time.sleep(delay)


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


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(16):
            pixel_index = (i * 256 // 16) + j
            pixels[i] = wheel(pixel_index & 255)
            pixels[31 - i] = wheel(pixel_index & 255)
            pixels[i + 31] = wheel(pixel_index & 255)
            pixels[63 - i] = wheel(pixel_index & 255)
        if runtime == 'Raspberry':
            pixels.show()
        elif runtime == 'ESP8266':
            pixels.write()
        time.sleep(wait)


while True:
    starting_func((255, 0, 0), 0.2)
    starting_func((0, 255, 0), 0.2)
    starting_func((0, 0, 255), 0.2)

    while True:
        rainbow_cycle(0.0001)
