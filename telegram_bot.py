#! /usr/bin//env python
# -*- coding: utf-8 -*-

import os
import logging
from decorator import decorator, decorate
from emoji import emojize
from subprocess import call
from telegram import ParseMode
from telegram.ext import CommandHandler, Updater, ConversationHandler

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(os.environ['TELEGRAM_TOKEN'])

SERVICES = ['homebridge', 'lirc', 'lamp_ir', 'dingdong']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

@decorator
def auth(f, bot, update, *args, **kwargs):
    if update.message.chat_id == int(CHAT_ID):
        f(bot, update, *args, **kwargs)
    else:
        update.message.reply_text(
            '%(emoji)s *UNAUTHORIZED* %(emoji)s' % {
                'emoji': emojize(':no_entry_sign:', use_aliases=True)
            }, 
            parse_mode=ParseMode.MARKDOWN
        )

def service(map_fn):
    @auth
    def wrapper(bot, update, args, *vargs, **kwargs):
        unknown_services = set(args) - set(SERVICES)
        if len(unknown_services) > 0:
            update.message.reply_text(
                'Uknown service%(s)s: ' % {'s': 's' if len(unknown_services) > 1 else ''} + 
                ', '.join(unknown_services)
            )
            return

        results = map(map_fn, args or SERVICES)
        update.message.reply_text('\n'.join(results), parse_mode=ParseMode.MARKDOWN)
    
    return wrapper

def service_status(service):
    running = call(['sudo', 'systemctl', 'status', service]) == 0
    return u'%(emoji)s *%(service)s* - %(status)s' % {
        'emoji': emojize(
            ':white_check_mark:' if running else ':no_entry_sign:',
            use_aliases=True
        ),
        'service': service,
        'status': 'Running' if running else 'Not running'
    }

@service
def service_start(service):
    call(['sudo', 'systemctl', 'start', service])
    return service_status(service)

@service
def service_stop(service):
    call(['sudo', 'systemctl', 'stop', service])
    return service_status(service)

def main() :
    status_handler = CommandHandler('status', service(service_status), pass_args=True)
    updater.dispatcher.add_handler(status_handler)

    start_service_handler = CommandHandler('start', service_start, pass_args=True)
    updater.dispatcher.add_handler(start_service_handler)

    stop_service_handler = CommandHandler('stop', service_stop, pass_args=True)
    updater.dispatcher.add_handler(stop_service_handler)

    updater.start_polling()
    updater.idle()

main()
