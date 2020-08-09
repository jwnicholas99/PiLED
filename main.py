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

def print_menu(is_construction=False):
    print("What LED pattern would you like to display?")
    print("1. Default")
    print("2. Color Wipe")
    print("3. Pulse")
    print("4. Wave")
    print("5. Rainbow Cycle")
    print("6. Rainbow Chase")
    
    if is_construction:
        print("7: End sequence")
    else:
        print("7. Construct your own")
        print("S. Shutdown")
    print("")

def ask_colors(args):
    colors = raw_input("Colors (comma separated - eg 255 255 255, 70 10 0): ").split(",")
    for color in colors:
        rgb = [int(x) for x in color.split()]
        args['colors'].append(Color(*rgb))

def action(option, args=None):
    if option == "1":
        moodlights.wave(colors, 255, spread=7)
        moodlights.wave(colors, 255, spread=7, is_reverse=True)
        moodlights.color_wipe(colors, 100)
        moodlights.pulse(5)
        moodlights.all_pixels_off()

    elif option == "2":
        if args is None:
            args = {"colors": [], 
                    "wait_ms": 0}
            ask_colors(args)
            args["wait_ms"] = int(raw_input("wait_ms for Color Wipe: "))
        moodlights.color_wipe(**args)

    elif option == "3":
        if args is None:
            args = {"iterations": 0} 
            args["iterations"] = int(raw_input("Num of iterations for Pulse (0 is infinite): "))
        moodlights.pulse(**args)

    elif option == "4":
        if args is None:
            args = {"colors": [],
                    "intensity": 0, 
                    "wait_ms": 0,
                    "spread": 0,
                    "is_reverse": False}
            ask_colors(args)
            args["wait_ms"] = int(raw_input("wait_ms for Wave: "))
            args["intensity"] = int(raw_input("Intensity of wave (between 0 and 255): "))
            args["spread"] = int(raw_input("spread for wave: "))
            args["is_reverse"] = bool(raw_input("is_reverse for wave: "))
        moodlights.wave(**args)

    elif option == "5":
        if args is None:
            args = {"iterations": 0, 
                    "wait_ms": 0}
            args["iterations"] = int(raw_input("Num of iterations for Rainbow Cycle: "))
            args["wait_ms"] = int(raw_input("wait_ms for Rainbow Cycle: "))
        moodlights.rainbow_cycle(**args)

    elif option == "6":
        if args is None:
            args = {"iterations": 0, 
                    "wait_ms": 0}
            args["iterations"] = int(raw_input("Num of iterations for Rainbow Cycle: "))
            args["wait_ms"] = int(raw_input("wait_ms for Rainbow Cycle: "))
        moodlights.rainbow_chase(**args)

    elif option == "S":
        moodlights.shutdown()


if  __name__=="__main__":
    parser = argparse.ArgumentParser(description="Control some LEDs")
    parser.add_argument("--led_count", type=int, default=30, help="Number of LED pixels")
    parser.add_argument("--led_pin", type=int, help="GPIO pin connected to the pixels")
    parser.add_argument("--led_brightness", type=int, help="Brightness of pixels (between 0 and 255)")
    parser.add_argument("--mood", type=str, help="Mood to set the lights to")
    args = parser.parse_args()

    # Create a Moodlight object
    moodlights = Moodlights(args.led_count, args.led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, args.led_brightness, LED_CHANNEL)

    # Ask for user raw_input
    while True:
        print_menu()
        option = raw_input("Option: ")

        colors = get_mood_colors(args.mood)
        action(option)
        


