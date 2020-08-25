import os
import copy
import tkinter as tk
from tkcolorpicker import askcolor
from tkinter import ttk
from tkinter import messagebox
from rpi_ws281x import Color, PixelStrip, ws

class GUI():
    def __init__(self, master, moodlights):
        self.moodlights = moodlights

        self.master = master
        master.title("RPi RGB")
        master.geometry("800x800")

        self.notebook = ttk.Notebook(master)
        self.notebook.enable_traversal()
        self.notebook.pack(fill="both", expand=1)

        color_wipe_notebook_frame = ttk.Frame(self.notebook, width=800, height=600)
        pulse_notebook_frame = ttk.Frame(self.notebook, width=800, height=600)
        wave_notebook_frame = ttk.Frame(self.notebook, width=800, height=600)
        rainbow_cycle_notebook_frame = ttk.Frame(self.notebook, width=800, height=600)
        rainbow_chase_notebook_frame = ttk.Frame(self.notebook, width=800, height=600)
        construct_notebook_frame = ttk.Frame(self.notebook, width=800, height=600)

        color_wipe_frame = self.create_canvas(color_wipe_notebook_frame)
        pulse_frame = self.create_canvas(pulse_notebook_frame)
        wave_frame = self.create_canvas(wave_notebook_frame)
        rainbow_cycle_frame = self.create_canvas(rainbow_cycle_notebook_frame)
        rainbow_chase_frame = self.create_canvas(rainbow_chase_notebook_frame)
        construct_frame = self.create_canvas(construct_notebook_frame)


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

        constructed_sequence = []
        constructed_sequence_frame = ttk.LabelFrame(construct_frame, text="Constructed Sequence")
        color_wipe_construct_button = ttk.Button(color_wipe_frame,
                                                 text="Add to Construction",
                                                 width="20", 
                                                 command=lambda: self.add_construction(constructed_sequence_frame,
                                                                                       constructed_sequence,
                                                                                       {
                                                                                         'pattern': 'color_wipe',
                                                                                         'color_sequence': color_wipe_sequence,
                                                                                         'iterations': color_wipe_iterations.get(),
                                                                                         'wait_ms': color_wipe_wait_ms.get()
                                                                                        }))
        color_wipe_construct_button.pack(pady=5)


        # Set up pulse frame
        pulse_params_frame = ttk.LabelFrame(pulse_frame, text="Parameters", padding=20)
        pulse_iterations = self.setup_entry(pulse_params_frame, "Num iterations (0 is infinite): ")
        pulse_wait_ms = self.setup_entry(pulse_params_frame, "Wait time (ms): ")

        pulse_params_frame.pack(pady=70)
        pulse_button = ttk.Button(pulse_frame, text="Display", width="20", 
                                       command=lambda: self.pulse(pulse_iterations.get(), pulse_wait_ms.get()))
        pulse_button.pack(pady=20)

        pulse_construct_button = ttk.Button(pulse_frame,
                                            text="Add to Construction",
                                            width="20", 
                                            command=lambda: self.add_construction(constructed_sequence_frame,
                                                                                  constructed_sequence,
                                                                                       {
                                                                                         'pattern': 'pulse',
                                                                                         'iterations': pulse_iterations.get(),
                                                                                         'wait_ms': pulse_wait_ms.get()
                                                                                        }))
        pulse_construct_button.pack(pady=5)

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

        wave_construct_button = ttk.Button(wave_frame,
                                            text="Add to Construction",
                                            width="20", 
                                            command=lambda: self.add_construction(constructed_sequence_frame,
                                                                                  constructed_sequence,
                                                                                       {
                                                                                         'pattern': 'wave',
                                                                                         'color_sequence': wave_sequence,
                                                                                         'iterations': wave_iterations.get(),
                                                                                         'intensity': wave_intensity.get(),
                                                                                         'wait_ms': wave_wait_ms.get(),
                                                                                         'spread': wave_spread.get(),
                                                                                         'is_reverse': wave_is_reverse.get()
                                                                                        }))
        wave_construct_button.pack(pady=5)


        # Set up rainbow cycle frame
        rainbow_cycle_params_frame = ttk.LabelFrame(rainbow_cycle_frame, text="Parameters", padding=20)
        rainbow_cycle_iterations = self.setup_entry(rainbow_cycle_params_frame, "Num iterations (0 is infinite): ")
        rainbow_cycle_wait_ms = self.setup_entry(rainbow_cycle_params_frame, "Wait time (ms): ")

        rainbow_cycle_params_frame.pack(pady=70)
        rainbow_cycle_button = ttk.Button(rainbow_cycle_frame, text="Display", width="20", 
                                       command=lambda: self.rainbow_cycle(rainbow_cycle_iterations.get(), rainbow_cycle_wait_ms.get()))
        rainbow_cycle_button.pack(pady=20)

        rainbow_cycle_construct_button = ttk.Button(rainbow_cycle_frame,
                                            text="Add to Construction",
                                            width="20", 
                                            command=lambda: self.add_construction(constructed_sequence_frame,
                                                                                  constructed_sequence,
                                                                                       {
                                                                                         'pattern': 'rainbow_cycle',
                                                                                         'iterations': rainbow_cycle_iterations.get(),
                                                                                         'wait_ms': rainbow_cycle_wait_ms.get()
                                                                                        }))
        rainbow_cycle_construct_button.pack(pady=5)

        # Set up rainbow chase frame
        rainbow_chase_params_frame = ttk.LabelFrame(rainbow_chase_frame, text="Parameters", padding=20)
        rainbow_chase_iterations = self.setup_entry(rainbow_chase_params_frame, "Num iterations (0 is infinite): ")
        rainbow_chase_wait_ms = self.setup_entry(rainbow_chase_params_frame, "Wait time (ms): ")

        rainbow_chase_params_frame.pack(pady=70)
        rainbow_chase_button = ttk.Button(rainbow_chase_frame, text="Display", width="20", 
                                       command=lambda: self.rainbow_chase(rainbow_chase_iterations.get(), rainbow_chase_wait_ms.get()))
        rainbow_chase_button.pack(pady=20)

        rainbow_chase_construct_button = ttk.Button(rainbow_chase_frame,
                                            text="Add to Construction",
                                            width="20", 
                                            command=lambda: self.add_construction(constructed_sequence_frame,
                                                                                  constructed_sequence,
                                                                                       {
                                                                                         'pattern': 'rainbow_chase',
                                                                                         'iterations': rainbow_chase_iterations.get(),
                                                                                         'wait_ms': rainbow_chase_wait_ms.get()
                                                                                        }))
        rainbow_chase_construct_button.pack(pady=5)

        constructed_sequence_frame.pack(pady=10)
        constructed_iterations = self.setup_entry(construct_frame, "Num iterations (0 is infinite): ")
        constructed_button = ttk.Button(construct_frame, text="Display", width="20", 
                                        command=lambda: self.display_construction(constructed_sequence, constructed_iterations.get()))
        constructed_button.pack(pady=30)


        color_wipe_notebook_frame.pack(fill="both", expand=1)
        pulse_notebook_frame.pack(fill="both", expand=1)
        wave_notebook_frame.pack(fill="both", expand=1)
        rainbow_cycle_notebook_frame.pack(fill="both", expand=1)
        rainbow_chase_notebook_frame.pack(fill="both", expand=1)
        construct_notebook_frame.pack(fill="both", expand=1)

        self.notebook.add(color_wipe_notebook_frame, text="Color Wipe")
        self.notebook.add(pulse_notebook_frame, text="Pulse")
        self.notebook.add(wave_notebook_frame, text="Wave")
        self.notebook.add(rainbow_cycle_notebook_frame, text="Rainbow Cycle")
        self.notebook.add(rainbow_chase_notebook_frame, text="Rainbow Chase")
        self.notebook.add(construct_notebook_frame, text="Construct")

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

    def color_wipe(self, sequence, iterations, wait_ms):
        sequence = convert_input(sequence, "color", "Color Wipe color sequence", "a non-empty list")
        iterations = convert_input(iterations, "int", "Color Wipe iterations", "a positive int")
        wait_ms = convert_input(wait_ms, "float", "Color Wipe wait_ms", "a positive float")
        if any([arg is None for arg in [sequence, iterations, wait_ms]]):
            return
        self.moodlights.color_wipe(sequence, iterations, wait_ms)

    def wave(self, sequence, iterations, intensity, wait_ms, spread, is_reverse):
        sequence = convert_input(sequence, "color", "Wave color sequence", "a non-empty list")
        iterations = convert_input(iterations, "int", "Wave iterations", "a positive int")
        intensity = convert_input(intensity, "intensity", "Wave intensity", "a positive int between 0 and 255")
        wait_ms = convert_input(wait_ms, "float", "Wave wait_ms", "a positive float")
        spread = convert_input(spread, "int", "Wave spread", "a positive int")
        is_reverse = convert_input(is_reverse, "bool", "Wave is_reverse", "a 'True' or 'False'")
        if any([arg is None for arg in [sequence, iterations, intensity, wait_ms, spread, is_reverse]]):
            return
        is_reverse = is_reverse == 'True'
        self.moodlights.wave(sequence, iterations, intensity, wait_ms, spread, is_reverse)

    def pulse(self, iterations, wait_ms):
        iterations = convert_input(iterations, "int", "Pulse iterations", "a positive int")
        wait_ms = convert_input(wait_ms, "float", "Pulse wait_ms", "a positive float")
        if any([arg is None for arg in [iterations, wait_ms]]):
            return
        self.moodlights.pulse(iterations, wait_ms)

    def rainbow_cycle(self, iterations, wait_ms):
        iterations = convert_input(iterations, "int", "Rainbow Cycle iterations", "a positive int")
        wait_ms = convert_input(wait_ms, "float", "Rainbow Cycle wait_ms", "a positive float")
        if any([arg is None for arg in [iterations, wait_ms]]):
            return
        self.moodlights.rainbow_cycle(iterations, wait_ms)

    def rainbow_chase(self, iterations, wait_ms):
        iterations = convert_input(iterations, "int", "Rainbow Chase iterations", "a positive int")
        wait_ms = convert_input(wait_ms, "float", "Rainbow Chase wait_ms", "a positive float")
        if any([arg is None for arg in [iterations, wait_ms]]):
            return
        self.moodlights.rainbow_chase(iterations, wait_ms)

    def display_construction(self, sequence, iterations):
        patterns = {
            "color_wipe": self.color_wipe,
            "pulse": self.pulse,
            "wave": self.wave,
            "rainbow_cycle": self.rainbow_cycle,
            "rainbow_chase": self.rainbow_chase
        }

        iterations = int(iterations)
        is_infinite = iterations == 0
        i = 0
        while is_infinite or i < iterations:
            for pattern_args in sequence:
                pattern = pattern_args['pattern']
                args = [v for k,v in pattern_args.items() if k not in ["pattern", "frame"]]
                patterns[pattern](*args)
            i += 1

    def bits2hex(self, bits):
        r = hex(bits >> 16 & 0xff)[2:].rjust(2, "0")
        g = hex(bits >> 8 & 0xff)[2:].rjust(2, "0")
        b = hex(bits & 0xff)[2:].rjust(2, "0")
        return "#" + r + g + b

    def add_construction(self, sequences_frame, constructed_sequence, args):
        container_frame = ttk.Frame(sequences_frame)
        pattern_frame = ttk.LabelFrame(container_frame, text=args["pattern"], padding=10)
        for key in args:
            if key == "color_sequence":
                color_sequence_frame = ttk.LabelFrame(pattern_frame, text="Color Sequence", padding=10)
                for color in args["color_sequence"]:
                    color_frame = tk.Frame(color_sequence_frame, width=15, height=15, bg=self.bits2hex(color)).pack(side=tk.LEFT)
                color_sequence_frame.pack(side=tk.LEFT, padx=5, pady=5)
            elif key == "pattern":
                continue
            else:
                arg_label = ttk.Label(pattern_frame, text=key + ": " + str(args[key]))
                arg_label.pack(side=tk.LEFT, padx=5)
        pattern_frame.pack(side=tk.LEFT, padx=10, pady=10)

        remove_button = ttk.Button(container_frame, text="Remove", command=lambda: self.remove_pattern(container_frame, constructed_sequence))
        remove_button.pack(side=tk.RIGHT, padx=5)
        container_frame.pack(fill="x", expand=1)

        construct_args = copy.deepcopy(args)
        construct_args["frame"] = container_frame
        constructed_sequence.append(construct_args)

    def remove_pattern(self, frame, sequence):
        for i in range(len(sequence)):
            if sequence[i]["frame"] is frame:
                sequence.pop(i)
                frame.destroy()
                break

    def create_canvas(self, notebook_frame):
        canvas = tk.Canvas(notebook_frame)
        canvas.pack(side=tk.LEFT, fill="both", expand=1)
        scrollbar = ttk.Scrollbar(notebook_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        inner_frame = ttk.Frame(canvas)
        canvas.create_window((400,0), window=inner_frame, anchor="n")

        return inner_frame

def convert_input(input, input_type, param_name, correct_type):
    def convert_bool(input):
        if input != "True" and input != "False":
            raise TypeError()
        return input

    def convert_int(input):
        output = int(input)
        if output < 0:
            raise TypeError()
        return output

    def convert_float(input):
        output = float(input)
        if output < 0.0:
            raise TypeError()
        return output

    def convert_intensity(input):
        output = int(input)
        if output < 0 or output > 255:
            raise TypeError()
        return output

    def convert_color(input):
        if not len(input):
            raise TypeError()
        return input

    types = {
        "int": convert_int,
        "float": convert_float,
        "bool": convert_bool,
        "intensity": convert_intensity,
        "color": convert_color
    }

    try:
        output = types[input_type](input)
        return output
    except:
        if os.environ.get('DISPLAY','') == '':
            print(param_name + " needs to be " + correct_type)
        else:
            messagebox.showerror("Invalid input", param_name + " needs to be " + correct_type)
        return None