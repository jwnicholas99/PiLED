<h1 align="center">
  <br>
  🌈 RPi RGB LED 
  <br>
</h1>

<h4 align="center">Point and click. Instant feedback. Effortless chaining.</h4>
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#setup">Setup</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

RPi RGB LED has a graphical user interface (GUI) for easy visualization. It also has pre-defined LED patterns which you can quickly chain together to create your own sequences.

## Key Features
There are three key features: 
1. Pre-defined LED patterns like `pulse` and `wave`
2. Easy chaining
3. GUI app which provides instant feedback as you are building your LED sequences

### Pre-defined LED Patterns
There are 5 pre-defined LED patterns:
1. Color Wipe
2. Pulse
3. Wave
4. Rainbow Cycle
5. Rainbow Chase

### Easy Chaining
To make even more awesome LED sequences, there is an option to construct your own sequences by chaining together the above pre-defined LED patterns. All you have to do is click a button to add the pre-defined LED pattern to your own LED sequence. 

### GUI App
When you want to create a color sequence, you can use a color picker to visually choose the color you want, rather than finding hex codes like '#808000' through trial and error.

After picking the color, the LED strip will immediately display the chosen color sequence so that you can instant feedback.

Finally, the app makes it easy to chain patterns together by adding your chosen LED patterns to the construction page.

## Usage
To launch with the GUI, run
```
sudo python3 main.py --led_count=30 --led_pin=18 --led_brightness=255
```
where `--led_count` is the number of pixels in your LED strip, and `--led_pin` is the RPi GPIO pin that you are using to control the LED strip. Take note that you need `sudo` for the `rpi_ws281x` library to work to access the underlying hardware.

The GUI app has 6 tabs, 5 for the pre-defined LED patterns, and 1 for constructing your own. Each tab for the pre-defined patterns contains all the fields you need to set in order to create the LED pattern. There are two buttons, `Display` and `Add to Construction`. `Display` simply lights up the LED strip with your pattern, while `Add to Construction` will add the LED pattern to your own constructed sequence. The constructed sequence will be shown in the last tab.


You can also use plain command-line by running
```
sudo python3 main.py --led_count=30 --led_pin=18 --led_brightness=255 --use_gui=False
```


## Setup

There are two parts to the set-up: wiring the circuit and installing required Python packages. Luckily, both are easy.

### Wiring the Circuit

You only need the following hardware:
* Raspberry Pi 4B
* WS2812 or SK6812 RGB LED strip
* Three jumper wires

Connect them according to the diagram below:


### Installing

Install the following packages:

```
$ sudo pip3 install rpi_ws281x
$ sudo pip3 install tkinter
$ sudo pip3 install ttkthemes
$ sudo pip3 install tkcolorpicker
```
That's all! 

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```


## Built With

* Python - This entire application is written in Python
* [rpi-ws281x-python](https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/library/rpi_ws281x/rpi_ws281x.py) - Used to handle all the low-level stuff of controlling the LED strip
* [Tkinter](https://docs.python.org/3/library/tkinter.html) - Used to create the GUI app

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Nicholas Lim Jing Wei** - *Initial work* - [jwnicholas99](https://github.com/jwnicholas99)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

