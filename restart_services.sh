#! /bin/sh

rm /root/.homebridge/accessories/cachedAccessories

systemctl restart homebridge
systemctl restart lirc
systemctl restart lamp_ir
