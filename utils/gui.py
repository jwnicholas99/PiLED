import tkinter as tk
from tkinter import ttk
from rpi_ws281x import Color, PixelStrip, ws

class GUI():
    def __init__(self, master, moodlights):
        self.moodlights = moodlights

        self.master = master
        master.title("RPi RGB")
        master.geometry("800x600")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack()

        color_wipe_frame = tk.Frame(self.notebook, width=800, height=600)
        pulse_frame = tk.Frame(self.notebook, width=800, height=600)
        wave_frame = tk.Frame(self.notebook, width=800, height=600)
        rainbow_cycle_frame = tk.Frame(self.notebook, width=800, height=600)
        rainbow_chase_frame = tk.Frame(self.notebook, width=800, height=600)
        construct_frame = tk.Frame(self.notebook, width=800, height=600)

        color_wipe_frame.pack(fill="both", expand=1)
        pulse_frame.pack(fill="both", expand=1)
        wave_frame.pack(fill="both", expand=1)
        rainbow_cycle_frame.pack(fill="both", expand=1)
        rainbow_chase_frame.pack(fill="both", expand=1)
        construct_frame.pack(fill="both", expand=1)

        self.notebook.add(color_wipe_frame, text="Color Wipe")
        self.notebook.add(pulse_frame, text="Pulse")
        self.notebook.add(wave_frame, text="Wave")
        self.notebook.add(rainbow_cycle_frame, text="Rainbow Cycle")
        self.notebook.add(rainbow_chase_frame, text="Rainbow Chase")
        self.notebook.add(construct_frame, text="Construct")

    def light(self):
        self.moodlights.wave([Color(100, 150, 50)], 255, spread=int(self.wave_spread_entry.get()))
