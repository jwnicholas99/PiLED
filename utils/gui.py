import tkinter as tk
from tkcolorpicker import askcolor
from tkinter import ttk
from rpi_ws281x import Color, PixelStrip, ws

class GUI():
    def __init__(self, master, moodlights):
        self.moodlights = moodlights

        self.master = master
        master.title("RPi RGB")
        master.geometry("800x600")

        self.notebook = ttk.Notebook(master)
        self.notebook.enable_traversal()
        self.notebook.pack()

        color_wipe_frame = ttk.Frame(self.notebook, width=800, height=600)
        pulse_frame = ttk.Frame(self.notebook, width=800, height=600)
        wave_frame = ttk.Frame(self.notebook, width=800, height=600)
        rainbow_cycle_frame = ttk.Frame(self.notebook, width=800, height=600)
        rainbow_chase_frame = ttk.Frame(self.notebook, width=800, height=600)
        construct_frame = ttk.Frame(self.notebook, width=800, height=600)

        # Set up color wipe frame
        color_wipe_sequence = []
        self.setup_pick_colors(color_wipe_frame, color_wipe_sequence)
        color_wipe_params_frame = ttk.LabelFrame(color_wipe_frame, text="Parameters", padding=20)
        color_wipe_iterations = self.setup_entry(color_wipe_params_frame, "Num iterations (0 is infinite): ")
        color_wipe_wait_ms = self.setup_entry(color_wipe_params_frame, "Wait time (ms): ")

        color_wipe_params_frame.pack(pady=10)
        color_wipe_button = ttk.Button(color_wipe_frame, text="Display", width="20", 
                                       command=lambda: self.color_wipe(color_wipe_sequence, color_wipe_iterations.get(), color_wipe_wait_ms.get()))
        color_wipe_button.pack(pady=20)


        # Set up pulse frame
        pulse_params_frame = ttk.LabelFrame(pulse_frame, text="Parameters", padding=20)
        pulse_iterations = self.setup_entry(pulse_params_frame, "Num iterations (0 is infinite): ")
        pulse_wait_ms = self.setup_entry(pulse_params_frame, "Wait time (ms): ")

        pulse_params_frame.pack(pady=70)
        pulse_button = ttk.Button(pulse_frame, text="Display", width="20", 
                                       command=lambda: self.pulse(pulse_iterations.get(), pulse_wait_ms.get()))
        pulse_button.pack(pady=20)


        # Set up wave frame
        wave_sequence = []
        self.setup_pick_colors(wave_frame, wave_sequence)

        wave_params_frame = ttk.LabelFrame(wave_frame, text="Parameters", padding=10)
        wave_iterations = self.setup_entry(wave_params_frame, "Num iterations (0 is infinite): ")
        wave_intensity = self.setup_entry(wave_params_frame, "Intensity (0-255): ")
        wave_wait_ms = self.setup_entry(wave_params_frame, "Wait time (ms): ")
        wave_spread = self.setup_entry(wave_params_frame, "Spread: ")
        wave_is_reverse = self.setup_entry(wave_params_frame, "Is reverse (True or False): ")

        wave_params_frame.pack(pady=0)
        wave_button = ttk.Button(wave_frame, text="Display", width="20", 
                                       command=lambda: self.wave(wave_sequence,
                                                                 wave_iterations.get(),
                                                                 wave_intensity.get(),
                                                                 wave_wait_ms.get(),
                                                                 wave_spread.get(),
                                                                 wave_is_reverse.get()))
        wave_button.pack(pady=10)



        # Set up rainbow cycle frame
        rainbow_cycle_params_frame = ttk.LabelFrame(rainbow_cycle_frame, text="Parameters", padding=20)
        rainbow_cycle_iterations = self.setup_entry(rainbow_cycle_params_frame, "Num iterations (0 is infinite): ")
        rainbow_cycle_wait_ms = self.setup_entry(rainbow_cycle_params_frame, "Wait time (ms): ")

        rainbow_cycle_params_frame.pack(pady=70)
        rainbow_cycle_button = ttk.Button(rainbow_cycle_frame, text="Display", width="20", 
                                       command=lambda: self.rainbow_cycle(rainbow_cycle_iterations.get(), rainbow_cycle_wait_ms.get()))
        rainbow_cycle_button.pack(pady=20)


        # Set up rainbow chase frame
        rainbow_chase_params_frame = ttk.LabelFrame(rainbow_chase_frame, text="Parameters", padding=20)
        rainbow_chase_iterations = self.setup_entry(rainbow_chase_params_frame, "Num iterations (0 is infinite): ")
        rainbow_chase_wait_ms = self.setup_entry(rainbow_chase_params_frame, "Wait time (ms): ")

        rainbow_chase_params_frame.pack(pady=70)
        rainbow_chase_button = ttk.Button(rainbow_chase_frame, text="Display", width="20", 
                                       command=lambda: self.rainbow_chase(rainbow_chase_iterations.get(), rainbow_chase_wait_ms.get()))
        rainbow_chase_button.pack(pady=20)



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

    def ask_color(self, frame, sequence):
        color = askcolor()
        if color[0] is not None:
            rgb = [int(x) for x in color[0]]
            sequence.append(Color(*rgb))
            self.moodlights.color_wipe(sequence, 1, 0)
            color_frame = tk.Frame(frame, width=20, height=20, bg=color[1]).pack(side=tk.LEFT)

    def remove_color(self, frame, sequence):
        colors = frame.winfo_children()
        if colors:
            sequence.pop()
            colors[-1].destroy()
            self.moodlights.color_wipe(sequence, 1, 0)

    def clear_color(self, frame, sequence):
        for color in frame.winfo_children():
            sequence.pop()
            color.destroy()
            self.moodlights.color_wipe([Color(0, 0, 0)], 1, 0)

    def setup_pick_colors(self, frame, sequence):
        pick_color_frame = ttk.LabelFrame(frame, text="Choose a color sequence", padding=20)
        sequence_frame = ttk.LabelFrame(pick_color_frame, text="Color Sequence", padding=10)
        buttons_frame = ttk.Frame(pick_color_frame, padding=10)
        add_color_button = ttk.Button(buttons_frame, text="Add color", command=lambda: self.ask_color(sequence_frame, sequence))
        remove_color_button = ttk.Button(buttons_frame, text="Remove color", command=lambda: self.remove_color(sequence_frame, sequence))
        clear_color_button = ttk.Button(buttons_frame, text="Clear", command=lambda: self.clear_color(sequence_frame, sequence))

        pick_color_frame.pack(pady=40)
        buttons_frame.pack()
        add_color_button.pack(side=tk.LEFT)
        remove_color_button.pack(side=tk.LEFT)
        clear_color_button.pack(side=tk.LEFT)
        sequence_frame.pack(padx=10, pady=10)

    def setup_entry(self, frame, display_text):
        iterations_frame = ttk.Frame(frame, padding=10)
        iterations_label = ttk.Label(iterations_frame, text=display_text)
        iterations_entry = ttk.Entry(iterations_frame)
        iterations_frame.pack()
        iterations_label.pack(side=tk.LEFT)
        iterations_entry.pack(side=tk.LEFT)
        return iterations_entry

    def setup_wait_ms(self, frame):
        wait_ms_frame = ttk.Frame(frame, padding=10)
        wait_ms_label = ttk.Label(wait_ms_frame, text="wait time (ms): ")
        wait_ms_entry = ttk.Entry(wait_ms_frame)
        wait_ms_frame.pack()
        wait_ms_label.pack(side=tk.LEFT)
        wait_ms_entry.pack(side=tk.LEFT)
        return wait_ms_entry

    def color_wipe(self, sequence, iterations, wait_ms):
        iterations = int(iterations)
        wait_ms = int(wait_ms)
        self.moodlights.color_wipe(sequence, iterations, wait_ms)

    def wave(self, sequence, iterations, intensity, wait_ms, spread, is_reverse):
        iterations = int(iterations)
        intensity = int(intensity)
        wait_ms = int(wait_ms)
        spread = int(spread)
        is_reverse = is_reverse == 'True'
        self.moodlights.wave(sequence, iterations, intensity, wait_ms, spread, is_reverse)

    def pulse(self, iterations, wait_ms):
        iterations = int(iterations)
        wait_ms = int(wait_ms)
        self.moodlights.pulse(iterations, wait_ms)

    def rainbow_cycle(self, iterations, wait_ms):
        iterations = int(iterations)
        wait_ms = int(wait_ms)
        self.moodlights.rainbow_cycle(iterations, wait_ms)

    def rainbow_chase(self, iterations, wait_ms):
        iterations = int(iterations)
        wait_ms = int(wait_ms)
        self.moodlights.rainbow_chase(iterations, wait_ms)

