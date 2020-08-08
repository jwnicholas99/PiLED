from rpi_ws281x import Color, PixelStrip, ws
import time
import argparse

from utils.moodlights import Moodlights


# LED strip configuration:
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0


def set_mood(mood, strip):
    if mood=="happy":
        pulse(strip, 5)
    elif mood=="sad":
        wave(strip, Color(0, 150, 50), 100, 0)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Control some LEDs")
    parser.add_argument("--led_count", type=int, default=30, help="Number of LED pixels")
    parser.add_argument("--led_pin", type=int, help="GPIO pin connected to the pixels")
    parser.add_argument("--led_brightness", type=int, help="Brightness of pixels (between 0 and 255)")
    parser.add_argument("--mood", type=str, help="Mood to set the lights to")
    args = parser.parse_args()

    # Create a Moodlight object
    moodlights = Moodlights(args.led_count, args.led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, args.led_brightness, LED_CHANNEL)
    moodlights.wave(255, 30, 60, 255, spread=7)
    moodlights.wave(255, 30, 60, 255, spread=7, is_reverse=True)
    moodlights.color_wipe(255, 30, 60)
    moodlights.pulse()
