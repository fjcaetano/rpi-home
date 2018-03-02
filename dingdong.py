#! /usr/bin/python

import os
import time
import RPi.GPIO as gpio
from datetime import datetime
from emoji import emojize
from telegram import Bot, ParseMode

IN = 26
OUT = 17
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(IN, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(OUT, gpio.OUT)

telegram = Bot(os.environ['TELEGRAM_TOKEN'])
last_time = time.time()

print "Starting - " + str(datetime.now())

while True:
    if (gpio.wait_for_edge(IN, gpio.FALLING, timeout=5000) is None) or \
            (time.time() - last_time < 1) or \
            (gpio.input(IN) == 1):
        continue

    # If bounces back too quickly, treat as false positive
    if gpio.wait_for_edge(IN, gpio.RISING, timeout=50) is not None:
        continue

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print "DING DONG - %(now)s" % locals()
    last_time = time.time()

    gpio.output(OUT, False)
    time.sleep(0.5)
    gpio.output(OUT, True)

    telegram.send_message(
        chat_id=CHAT_ID,
        text='%(emoji)s _ding dong_' % {
            'emoji': emojize(':bell:', use_aliases=True)
        },
        parse_mode=ParseMode.MARKDOWN
    )

gpio.cleanup()
