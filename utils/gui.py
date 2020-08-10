import tkinter as tk
from rpi_ws281x import Color, PixelStrip, ws

class GUI():
    def __init__(self, master, moodlights):
        self.moodlights = moodlights

        self.master = master
        master.title("RPi RGB")
        master.geometry("1000x800")

        self.wave_color = tk.Label(text="What color?")
        self.wave_color.grid(column=0, row=0)
        self.wave_color_entry = tk.Entry()
        self.wave_color_entry.grid(column=1, row=0)

        self.wave_spread = tk.Label(text="What spread?")
        self.wave_spread.grid(column=0, row=1)
        self.wave_spread_entry = tk.Entry()
        self.wave_spread_entry.grid(column=1, row=1)

        self.button = tk.Button(master, text="Light", command=self.light)
        self.button.grid(column=0, row=2)

    def light(self):
        self.moodlights.wave([Color(255, 255, 255)], 255, spread=int(self.wave_spread_entry.get()))
