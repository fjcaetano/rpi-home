# RPi Home

Small RPi project for home automation.

- Control lamps with HomeKit and infrared.
- Get notified when the doorbell rings
- Telegram bot for status, logs, notifications and service management

## Manual Dependencies (Linux Only)

- [Homebridge](https://github.com/nfarina/homebridge)
- [Homebridge GPIO WPi2](https://github.com/rsg98/homebridge-gpio-wpi2)
- [lirc](http://www.lirc.org/)
- [Python lirc](https://github.com/tompreston/python-lirc)

## Usage

1. Install the dependencies
2. Configure your IR remote with using lirc's [irrecord](http://www.lirc.org/html/irrecord.html).
3. Start homebridge
4. Run `lamp_ir.py`

lirc is configured to work with 3 colored keys in the IR remote, each toggling
a relay.

### Telegram Bot

1. Create a bot by talking to [@BotFather](https://telegram.me/botfather)
2. Export your API token as `TELEGRAM_TOKEN`
3. Export a csv of authorized chat_ids as `TELEGRAM_CHAT_IDS`
4. Run `telegram_bot.py`
5. Run `dingdong.py`
