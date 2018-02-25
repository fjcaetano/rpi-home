#! /usr/bin/python

import os
import time
import RPi.GPIO as gpio
from pushover import Client
from datetime import datetime\

IN = 26
OUT = 17

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(IN, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(OUT, gpio.OUT)

pushover = Client(os.environ['PUSHOVER_USER'], api_token=os.environ['PUSHOVER_TOKEN'])
last_time = time.time()

while True:
    if (gpio.wait_for_edge(IN, gpio.FALLING, timeout=5000) is None) or \
            (time.time() - last_time < 1) or \
            (gpio.input(IN) == 1):
        continue

    print "\aDING DONG - " + str(datetime.now())
    last_time = time.time()
    pushover.send_message("Campainha tocou!", title="Home")

    gpio.output(OUT, True)
    time.sleep(0.5)
    gpio.output(OUT, False)

gpio.cleanup()
