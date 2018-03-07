#! /usr/bin/python

import lirc

import RPi.GPIO as gpio
import sys

PINS = {
	'RED': 2, # TV
	'GREEN': 3, # Mesa
	'YELLOW': 4 # Porta
}

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
[ gpio.setup(pin, gpio.OUT) for pin in PINS.values() ]

lirc.init("lamps")
lirc.load_config_file("lircrc")

while True:
	next_code = lirc.nextcode()
	if len(next_code) == 0:
		continue

	pin = next_code[0]

	newValue = not gpio.input(PINS[pin])
	gpio.output(PINS[pin], newValue)

	print "Turning " + pin + " lamp " + ("on" if newValue else "off")

lirc.deinit()
gpio.cleanup()
