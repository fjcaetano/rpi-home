#! /usr/bin/python

import logging
import os
import time
import RPi.GPIO as gpio
from datetime import datetime
from emoji import emojize
from telegram import Bot, ParseMode

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

IN = 26
OUT = 17
CHAT_IDS = map(int, os.environ['TELEGRAM_CHAT_IDS'].split(','))
TIME_RANGE = range(9, 22)

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(IN, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(OUT, gpio.OUT)
gpio.output(OUT, True)

telegram = Bot(os.environ['TELEGRAM_TOKEN'])
last_time = time.time()

logging.info("Starting - " + str(datetime.now()))

while True:
    if (gpio.wait_for_edge(IN, gpio.FALLING, timeout=5000) is None) or \
            (time.time() - last_time < 1) or \
            (gpio.input(IN) == 1):
        continue

    # If bounces back too quickly, treat as false positive
    if gpio.wait_for_edge(IN, gpio.RISING, timeout=100) is not None:
        logging.debug('False positive')
        continue

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logging.info("DING DONG - %(now)s" % locals())
    last_time = time.time()

    if datetime.now().hour in TIME_RANGE:
        # Only rings bell if hour between 9~22
        gpio.output(OUT, False)
        time.sleep(0.5)
        gpio.output(OUT, True)

    for chat_id in CHAT_IDS:
        logging.debug("Sending message")
        telegram.send_message(
            chat_id=chat_id,
            text='%(emoji)s _ding dong_' % {
                'emoji': emojize(':bell:', use_aliases=True)
            },
            parse_mode=ParseMode.MARKDOWN
        )

gpio.cleanup()
