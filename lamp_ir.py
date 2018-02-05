#! /usr/bin/python

import lirc

import RPi.GPIO as gpio
import sys

PINS = {
	'RED': 2,
	'GREEN': 3,
	'YELLOW': 4,
	'BLUE': 17
}

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
[ gpio.setup(pin, gpio.OUT) for pin in PINS.values() ]

sockid = lirc.init("lamps")

while True:
	pin = lirc.nextcode()[0]
	
	newValue = not gpio.input(PINS[pin])
	gpio.output(PINS[pin], newValue)

	print "Turning " + pin + " lamp " + ("on" if newValue else "off")

lirc.deinit() 
