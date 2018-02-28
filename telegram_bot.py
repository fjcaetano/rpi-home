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

def service(f):
    @auth
    def wrapper(bot, update, args, *vargs, **kwargs):
        unknown_services = set(args) - set(SERVICES)
        if len(unknown_services) > 0:
            update.message.reply_text(
                'Uknown service%(s)s: ' % {'s': 's' if len(unknown_services) > 1 else ''} + 
                ', '.join(unknown_services)
            )
            return

        f(bot, update, args, *vargs[1:], **kwargs)
    
    return wrapper

@service
def status(bot, update, args):
    def map_results(service):
        running = call(['echo', service]) == 0
        return u'%(emoji)s *%(service)s* - %(status)s' % {
            'emoji': emojize(
                ':white_check_mark:' if running else ':no_entry_sign:',
                use_aliases=True
            ),
            'service': service,
            'status': 'Running' if running else 'Not running'
        }

    results = map(map_results, args or SERVICES)
    update.message.reply_text('\n'.join(results), parse_mode=ParseMode.MARKDOWN)

@service
def start_service(bot, update, args):
    def map_results(service):
        call(['sudo', 'systemctl', 'start', service])
        return status.map_results(service)

    results = map(map_results, args or SERVICES)
    update.message.reply_text('\n'.join(results), parse_mode=ParseMode.MARKDOWN)


def main() :
    status_handler = CommandHandler('status', status, pass_args=True)
    updater.dispatcher.add_handler(status_handler)

    start_service_handler = CommandHandler('start_service', status, pass_args=True)
    updater.dispatcher.add_handler(start_service_handler)

    updater.start_polling()
    updater.idle()

# status(None, None, [])
main()
