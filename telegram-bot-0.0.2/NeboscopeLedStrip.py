import time
import threading
import neopixel
import board
from datetime import datetime, timedelta


class LedStrip:
    RED_STEP_FILL = 0
    GREEN_STEP_FILL = 1
    BLUE_STEP_FILL = 2
    RAINBOW_CYCLE = 3
    ALERT_ROTATING_RED = 4
    ALERT_ROTATING_BLUE = 5
    ALERT_ROTATING_RB = 6
    ALERT_BLINCKING_RED = 7
    ALERT_BLINCKING_BLUE = 8
    ALERT_BLINCKING_RB = 9
    ALERT_SWAPING_RED = 10
    ALERT_SWAPING_BLUE = 11
    ALERT_SWAPING_RB = 12
    SNOWFALL = 13

    def __init__(self):
        pixel_pin = board.D18
        self.pixels = neopixel.NeoPixel(
            pixel_pin, 64, brightness=1, auto_write=False, pixel_order=neopixel.GRB
        )
        self.thread = object
        self.end_flag = False
        self.check = True

    def effect(self, effect_name, seconds=-1, cycles=-1, clear=False, daemon=True):
        try:
            self.end_flag = True
        finally:
            func = {self.RED_STEP_FILL: self._red_step_fill, self.GREEN_STEP_FILL: self._green_step_fill,
                    self.BLUE_STEP_FILL: self._blue_step_fill, self.RAINBOW_CYCLE: self._rainbow_cycle,
                    self.ALERT_ROTATING_RED: self._rotating_red, self.ALERT_ROTATING_BLUE: self._rotating_blue,
                    self.ALERT_ROTATING_RB: self._rotating_rb}[effect_name]
            # , self.SNOWFALL: self._snowfall + matrix
            self.end_flag = False   
            if daemon:
                if clear:
                    self.thread = threading.Thread(target=self._clear_wrapper, args=(func, seconds, cycles),
                                                   daemon=True).start()
                else:
                    self.thread = threading.Thread(target=func, args=(seconds, cycles), daemon=True).start()
            else:
                if clear:
                    self._clear_wrapper(func, seconds, cycles)
                else:
                    func(seconds, cycles)

    def stop(self, clear=False):
        try:
            self.end_flag = True
            time.sleep(1)
            if clear:
                self.clear()
            return True
        except:
            return False

    def clear(self):
        self._fill((0, 0, 0), 0)

    def _clear_wrapper(self, function, seconds, cycles):
        function(seconds, cycles)
        self.clear()

    def _fill(self, color, delay=0.2):
        self.pixels.fill(color)
        self.pixels.show()
        time.sleep(delay)

    def _step_fill(self, color, seconds, cycles, delay=0.2):
        end = datetime.now() + timedelta(seconds=seconds)
        while True:
            if cycles != -1:
                if cycles == 0:
                    return
                cycles -= 1
            for i in range(16):
                if seconds != -1:
                    if datetime.now() >= end:
                        return
                if self.end_flag:
                    return
                self.pixels[i] = color
                self.pixels[31 - i] = color
                self.pixels[i + 31] = color
                self.pixels[63 - i] = color
                self.pixels.show()
                time.sleep(delay)

    def _red_step_fill(self, seconds, cycles):
        self._step_fill((255, 0, 0), seconds, cycles)

    def _green_step_fill(self, seconds, cycles):
        self._step_fill((0, 255, 0), seconds, cycles)

    def _blue_step_fill(self, seconds, cycles):
        self._step_fill((0, 0, 255), seconds, cycles)

    @staticmethod
    def _wheel(pos):
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
        return r, g, b

    def _rainbow_cycle(self, seconds, cycles, wait=0.1):
        end = datetime.now() + timedelta(seconds=seconds)
        while True:
            if cycles != -1:
                if cycles == 0:
                    return
                cycles -= 1
            for j in range(255):
                if seconds != -1:
                    if datetime.now() >= end:
                        return
                if self.end_flag:
                    return
                for i in range(16):
                    pixel_index = (i * 256 // 16) + j
                    self.pixels[i] = self._wheel(pixel_index & 255)
                    self.pixels[31 - i] = self._wheel(pixel_index & 255)
                    self.pixels[i + 31] = self._wheel(pixel_index & 255)
                    self.pixels[63 - i] = self._wheel(pixel_index & 255)
                self.pixels.show()
                time.sleep(wait)

    def _rotating(self, color1, color2, seconds, cycles, delay=0.2):
        end = datetime.now() + timedelta(seconds=seconds)
        while True:
            if cycles != -1:
                if cycles == 0:
                    return
                cycles -= 1
            for i in range(4):
                if seconds != -1:
                    if datetime.now() >= end:
                        return
                if self.end_flag:
                    return
                if i == 0:
                    for j in range(16):
                        self.pixels[j] = color1
                        self.pixels[31 - j] = (0, 0, 0)
                        self.pixels[j + 31] = color2
                        self.pixels[63 - j] = (0, 0, 0)
                elif i == 1:
                    for j in range(16):
                        self.pixels[j] = (0, 0, 0)
                        self.pixels[31 - j] = color1
                        self.pixels[j + 31] = (0, 0, 0)
                        self.pixels[63 - j] = color2
                elif i == 2:
                    for j in range(16):
                        self.pixels[j] = color2
                        self.pixels[31 - j] = (0, 0, 0)
                        self.pixels[j + 31] = color1
                        self.pixels[63 - j] = (0, 0, 0)
                elif i == 3:
                    for j in range(16):
                        self.pixels[j] = (0, 0, 0)
                        self.pixels[31 - j] = color2
                        self.pixels[j + 31] = (0, 0, 0)
                        self.pixels[63 - j] = color1
                self.pixels.show()
                time.sleep(delay)

    def _rotating_red(self, seconds, cycles):
        self._rotating((255, 0, 0), (0, 0, 0), seconds, cycles)

    def _rotating_blue(self, seconds, cycles):
        self._rotating((0, 0, 255), (0, 0, 0), seconds, cycles)

    def _rotating_rb(self, seconds, cycles):
        self._rotating((255, 0, 0), (0, 0, 255), seconds, cycles)

