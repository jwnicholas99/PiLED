from rpi_ws281x import Color, PixelStrip, ws
import time
import argparse
import tkinter as tk

from utils.moodlights import Moodlights
from utils.gui import GUI


# LED strip configuration:
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0


def get_mood_colors(mood):
    mood = mood.lower()
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
    print("What LED pattern would you like to display (Key in number or letter)?")
    print("1. Color Wipe")
    print("2. Pulse")
    print("3. Wave")
    print("4. Rainbow Cycle")
    print("5. Rainbow Chase")
    
    if is_construction:
        print("e: End sequence")
    else:
        print("6. Construct your own")
        print("m. Mood")
        print("s. Shutdown")
    print("")

def ask_colors(args):
    colors = input("Colors (comma separated - eg 255 255 255, 70 10 0): ").split(",")
    for color in colors:
        rgb = [int(x) for x in color.split()]
        args['colors'].append(Color(*rgb))

def action(option, args=None, is_construction=False):
    if option == "1":
        if args is None:
            args = {"colors": [], 
                    "wait_ms": 0}
            ask_colors(args)
            args["wait_ms"] = int(input("wait_ms for Color Wipe: "))

        if is_construction:
            return args
        moodlights.color_wipe(**args)

    elif option == "2":
        if args is None:
            args = {"iterations": 0, "wait_ms": 0} 
            args["iterations"] = int(input("Num of iterations for Pulse (0 is infinite): "))
            args["wait_ms"] = int(input("wait_ms for pulse: "))

        if is_construction:
            return args
        moodlights.pulse(**args)

    elif option == "3":
        if args is None:
            args = {"colors": [],
                    "intensity": 0, 
                    "wait_ms": 0,
                    "spread": 0,
                    "is_reverse": False}
            ask_colors(args)
            args["wait_ms"] = int(input("wait_ms for Wave: "))
            args["intensity"] = int(input("Intensity of wave (between 0 and 255): "))
            args["spread"] = int(input("spread for wave: "))
            args["is_reverse"] = input("is_reverse for wave (True or False): ") == "True"

        if is_construction:
            return args
        moodlights.wave(**args)

    elif option == "4":
        if args is None:
            args = {"iterations": 0, 
                    "wait_ms": 0}
            args["iterations"] = int(input("Num of iterations for Rainbow Cycle: "))
            args["wait_ms"] = int(input("wait_ms for Rainbow Cycle: "))

        if is_construction:
            return args
        moodlights.rainbow_cycle(**args)

    elif option == "5" :
        if args is None:
            args = {"iterations": 0, 
                    "wait_ms": 0}
            args["iterations"] = int(input("Num of iterations for Rainbow Chase: "))
            args["wait_ms"] = int(input("wait_ms for Rainbow Chase: "))

        if is_construction:
            return args
        moodlights.rainbow_chase(**args)

    elif option == "6" and not is_construction:
        cur_seq_option = ""
        seq = []
        seq_args = []
        while cur_seq_option != "e":
            print_menu(is_construction=True)
            cur_seq_option = input("Construction Option: ")
            if cur_seq_option != "e":
                seq.append(cur_seq_option)
                seq_args.append(action(cur_seq_option, is_construction=True))

        iterations = int(input("Num iterations of constructed sequence (infinite if 0): "))
        is_infinite = iterations == 0
        cur_iteration = 0

        while is_infinite or cur_iteration < iterations:
            for i in range(len(seq)):
                action(seq[i], seq_args[i])
            cur_iteration += 1

    elif option == "m" and not is_construction:
        mood = input("Mood (Happy, Excited, Romantic): ")
        colors = get_mood_colors(mood)

        iterations = int(input("Num iterations in mood sequence: "))
        is_infinite = iterations == 0
        cur_iteration = 0

        while is_infinite or cur_iteration < iterations:
            moodlights.wave(colors, 255, spread=7)
            moodlights.wave(colors, 255, spread=7, is_reverse=True)
            moodlights.color_wipe(colors, 100)
            moodlights.pulse(3)
            cur_iteration += 1


    elif option == "s" and not is_construction:
        moodlights.shutdown()

    else: 
        print("Not a valid option")

if  __name__=="__main__":
    parser = argparse.ArgumentParser(description="Control some LEDs")
    parser.add_argument("--led_count", type=int, default=30, help="Number of LED pixels")
    parser.add_argument("--led_pin", type=int, help="GPIO pin connected to the pixels")
    parser.add_argument("--led_brightness", type=int, help="Brightness of pixels (between 0 and 255)")
    parser.add_argument("--use_gui", type=bool, default=True, help="If True, launch Tkinter GUI. If False, use command line")
    args = parser.parse_args()

    # Create a Moodlight object
    moodlights = Moodlights(args.led_count, args.led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, args.led_brightness, LED_CHANNEL)

    if args.use_gui:
        root = tk.Tk()
        gui = GUI(root, moodlights)
        root.mainloop()
    else:
        # Ask for user input
        while True:
            print_menu()
            option = input("Option: ")
            action(option)
