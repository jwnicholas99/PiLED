import tkinter as tk
from rpi_ws281x import Color, PixelStrip, ws

class GUI():
    def __init__(self, master, moodlights):
        self.moodlights = moodlights

        self.master = master
        master.title("RPi RGB")
        master.geometry("1000x800")

        self.button = tk.Button(master, text="Light", command=self.light)
        self.button.pack()

    def light(self):
        self.moodlights.wave([Color(255, 255, 255)], 255, spread=7)
