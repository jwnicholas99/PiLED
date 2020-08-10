<h1 align="center">
  <br>
  🌈 RPi RGB LED 
  <br>
</h1>

<h4 align="center">Easy control of a RGB LED strip.</h4>
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#setup">Setup</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

RPi RGB LED has pre-defined LED patterns which you can quickly chain together to create your own sequences.

This is built on top of the [`rpi-ws281x`](https://github.com/rpi-ws281x/rpi-ws281x-python) library.

## Key Features

## Usage

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

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

