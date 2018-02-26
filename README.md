# RPi IR Lamps

Small RPi project to control lamps with HomeKit and infrared

## Dependencies

- [Homebridge](https://github.com/nfarina/homebridge)
- [Homebridge GPIO WPi2](https://github.com/rsg98/homebridge-gpio-wpi2)
- [lirc](http://www.lirc.org/)
- [Python lirc](https://github.com/tompreston/python-lirc)
- [Python Pushover](https://github.com/Thibauth/python-pushover)

## Usage

1. Install the dependencies
2. Configure your IR remote with using lirc's [irrecord](http://www.lirc.org/html/irrecord.html).
3. Start homebridge
4. Run `lamp_ir.py`

lirc is configured to work with 4 colored keys in the IR remote, each toggling
a relay.
