#! /bin/sh

systemctl stop homebridge
systemctl stop lirc
systemctl stop lamp_ir

rm /root/.homebridge/accessories/cachedAccessories

systemctl start homebridge
systemctl start lirc
systemctl start lamp_ir
