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


def get_mood_colors(mood):
    if mood=="happy":
        return [
            Color(1, 190, 254),
            Color(255, 221, 0),
            Color(255, 125, 0),
            Color(255, 0, 109),
            Color(173, 255, 2),
            Color(143, 0, 255)
        ]
    elif mood=="excited":
        return [
            Color(255, 221, 0),
            Color(255, 70, 0),
        ]
    elif mood=="romantic":
        return [
            Color(255, 30, 30),
            Color(255, 0, 109),
            Color(240, 85, 88),
            Color(249, 226, 220)
        ]

def print_menu():
    print("What LED pattern would you like to display?")
    print("1. Default")
    print("2. ColorWipe")
    print("3. Pulse")
    print("4. Wave")
    print("5. Rainbow Cycle")
    print("6. Rainbow Chase")

if  __name__=="__main__":
    parser = argparse.ArgumentParser(description="Control some LEDs")
    parser.add_argument("--led_count", type=int, default=30, help="Number of LED pixels")
    parser.add_argument("--led_pin", type=int, help="GPIO pin connected to the pixels")
    parser.add_argument("--led_brightness", type=int, help="Brightness of pixels (between 0 and 255)")
    parser.add_argument("--mood", type=str, help="Mood to set the lights to")
    args = parser.parse_args()

    # Create a Moodlight object
    moodlights = Moodlights(args.led_count, args.led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, args.led_brightness, LED_CHANNEL)

    # Ask for user input
    while True:
        print_menu()
        option = input("")

        colors = get_mood_colors(args.mood)
        if option == 1:
            moodlights.wave(colors, 255, spread=7)
            moodlights.wave(colors, 255, spread=7, is_reverse=True)
            moodlights.color_wipe(colors, 100)
            moodlights.pulse(5)
            moodlights.all_pixels_off()
        elif option == 2:
            moodlights.color_wipe(colors, 100)
        elif option == 3:
            moodlights.pulse(5)
        elif option == 4:
            moodlights.wave(colors, 255, spread=7)
        elif option == 5:
            moodlights.rainbow_cycle()
        elif option == 6:
            moodlights.rainbow_chase()



