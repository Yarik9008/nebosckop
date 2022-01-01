import time
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, 64, brightness=0.5, auto_write=False, pixel_order=ORDER
)


def starting_func(color, delay):
    for i in range(16):
        pixels[i] = color
        pixels[i + 16] = color
        pixels[i + 32] = color
        pixels[i + 48] = color
        pixels.show()
        time.sleep(delay)


def fill(color, delay):
    pixels.fill(color)
    pixels.show()
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
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(16):
            pixel_index = (i * 256 // 16) + j
            pixels[i] = wheel(pixel_index & 255)
            pixels[i + 16] = wheel(pixel_index & 255)
            pixels[i + 32] = wheel(pixel_index & 255)
            pixels[i + 48] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    fill((255, 0, 0), 1)
    fill((0, 255, 0), 1)
    fill((0, 0, 255), 1)

    starting_func((255, 0, 0), 0.2)
    starting_func((0, 255, 0), 0.2)
    starting_func((0, 0, 255), 0.2)

    rainbow_cycle(0.001)
