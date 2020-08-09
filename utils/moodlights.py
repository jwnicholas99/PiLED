from rpi_ws281x import Color, PixelStrip, ws
from utils.pixel import Pixel
import time

import signal
import sys
import atexit

class Moodlights():
    def __init__(self, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel):
        self.strip = PixelStrip(led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel)
        self.strip.begin()

        self.led_count = led_count
        self.pixels = [Pixel(self.strip, x) for x in range(led_count)]

        signal.signal(signal.SIGINT, self.signal_handler)

    def in_range(self, led_num):
        return led_num >= 0 and led_num < self.led_count

    def shutdown(self):
        self.all_pixels_off()
        sys.exit()

    def signal_handler(self, sig, frame):
        print("You pressed Ctrl-C! Exiting...")
        self.shutdown()
            
    def all_pixels_off(self):
        for pixel in self.pixels:
            pixel.switch_off()
        self.strip.show()

    def color_wipe(self, colors, wait_ms=0):
        """
        params:

        colors: sequence of colors to display
        wait_ms: wait time between each pixel (0 for instant)
        """
        for i in range(self.led_count):
            pixel = self.pixels[i]
            pixel.set_color(colors[i % len(colors)])
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def pulse(self, iterations=0, wait_ms=2):
        """
        params:

        iteration: number of pulses (0 means infinite)
        wait_ms: wait time before changing brightness by 1/255 of max brightness
        """
        is_increasing = self.strip.getBrightness() < 255
        is_infinite = iterations == 0

        i = 0
        while is_infinite or i < iterations * 256 * 2:
            if is_increasing:
                next_brightness = self.strip.getBrightness() + 1
                is_increasing = next_brightness != 255
            else:
                next_brightness = self.strip.getBrightness() - 1
                is_increasing = next_brightness == 0

            self.strip.setBrightness(next_brightness)
            time.sleep(wait_ms /1000.0)
            self.strip.show()
            i += 1

    def wave(self, colors, intensity, wait_ms=50, spread=0, is_reverse=False):
        """
        params:

        colors: sequence of colors to display
        intensity: brightness of the crest (from 0 to 255)
        wait_ms: wait time before the crest of the wave shifts
        spread: how many pixels away from the crest will be lighted up
        """
        intensity_interval = float(intensity / (spread + 1))
        led_iteration = range(-1 - spread, self.strip.numPixels() + spread + 1)
        if is_reverse:
            led_iteration.reverse()

        for i in led_iteration:
            if self.in_range(i):
                self.pixels[i].set_color(colors[i % len(colors)])
                self.pixels[i].set_brightness(intensity)

            for j in range(1, spread+1):
                brightness = int(abs(intensity - intensity_interval * j))

                if self.in_range(i-j):
                    self.pixels[i-j].set_color(colors[(i-j) % len(colors)])
                    self.pixels[i-j].set_brightness(brightness)
                if self.in_range(i+j):
                    self.pixels[i+j].set_color(colors[(i+j) % len(colors)])
                    self.pixels[i+j].set_brightness(brightness)
            
            if self.in_range(i - spread - 1):
                self.pixels[i-spread-1].switch_off()
            if self.in_range(i + spread + 1):
                self.pixels[i+spread+1].switch_off()
            self.strip.show()

            time.sleep(wait_ms / 1000.0)

    def wheel(self, pos):
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow_cycle(self, iterations=0, wait_ms=160):
        is_infinite = iterations == 0

        j = 0
        while is_infinite or j < iterations * 256:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            j += 1
            time.sleep(wait_ms / 1000)

    def rainbow_chase(self, iterations=0, wait_ms=100):
        is_infinite = iterations == 0

        j = 0
        while is_infinite or j < iterations * 256:
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)
            j += 1
        
