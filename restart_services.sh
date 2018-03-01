#! /bin/sh

updated_recently() {
  NOW=$(date +'%Y-%m-%d %H:%M')
  FILE_DATE=$(date -r $1 +'%Y-%m-%d %H:%M')

  echo "$1 - $FILE_DATE"

  [ "$NOW" = "$FILE_DATE" ]
}

echo "Restart services - $(date +'%Y-%m-%d %H:%M')"

if updated_recently 'homebridge.config'; then
  echo "Restarting Homebridge"
  rm /root/.homebridge/accessories/cachedAccessories
  systemctl restart homebridge
fi

if updated_recently 'lircrc'; then
  echo "Restarting lirc"
  systemctl restart lirc
fi

if updated_recently 'lamp_ir.py'; then
  echo "Restarting lamp_ir"
  systemctl restart lamp_ir
fi

if updated_recently 'dingdong.py'; then
  echo "Restarting dingdong"
  systemctl restart dingdong
fi