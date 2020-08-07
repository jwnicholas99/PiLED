import time
import rpi_ws281x

class Pixel():
    def __init__(self, strip, pixel_num):
        self.strip = strip
        self.pixel_num = pixel_num

    def switch_off(self):
        self.strip.setPixelColorRGB(self.pixel_num, 0, 0, 0)

    def get_brightness(self):
        """
        A pixel's brightness is different from it's color because
        brightness is about the intensity of RGB, while color is the 
        ratio between RGB colors. To determine the brightness, we
        pick the highest intensity.

        eg. 'RGB: 40 20 20' and 'RGB: 80 40 40' has the same color,
        but different brightness
        """
        cur_color = self.strip.getPixelColorRGB(self.pixel_num)
        return max(cur_color.r, cur_color.g, cur_color.b)

    def set_brightness(self, intensity):
        """
        In order to increase the intensity and keep the same color,
        we need to keep track of the ratio of RGB colors

        params:

        intensity: intensity of pixel's brightness to be set to
        """
        cur_color = self.strip.getPixelColorRGB(self.pixel_num)
        highest_intensity = float(max(cur_color.r, cur_color.g, cur_color.b))
        factor = intensity / highest_intensity
        new_r = int(cur_color.r * factor)
        new_g = int(cur_color.g * factor)
        new_b = int(cur_color.b * factor)

        self.strip.setPixelColorRGB(self.pixel_num, new_r, new_g, new_b)
        self.strip.show()

    def change_brightness(self, intensity):
        """
        Params:

        intensity - how much to change the brightness by (value from 0 to 255)
        """
        cur_brightness = self.get_brightness()
        new_brightness = cur_brightness + intensity
        if new_brightness > 255:
            new_brightness = 255
        if new_brightness < 0:
            new_brightness = 0

        self.set_brightness(new_brightness)
        self.strip.show()
        
