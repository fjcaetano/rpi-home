#! /bin/sh

updated_recently() {
  NOW=$(date +'%Y-%m-%d %H:%M')
  FILE_DATE=$(date -r $1 +'%Y-%m-%d %H:%M')

  [ "$NOW" = "$FILE_DATE" ]
}

if updated_recently 'requirements.txt'; then
  source venv/bin/activate
  pip install -r requirements.txt
fi

if updated_recently 'homebridge.config'; then
  echo "Restarting Homebridge"
  rm /root/.homebridge/accessories/cachedAccessories
  sudo systemctl stop homebridge
  sudo systemctl start homebridge
fi

if updated_recently 'lircrc'; then
  echo "Restarting lirc"
  sudo systemctl stop lirc
  sudo systemctl start lirc
fi

if updated_recently 'lamp_ir.py'; then
  echo "Restarting lamp_ir"
  sudo systemctl stop lamp_ir
  sudo systemctl start lamp_ir
fi

if updated_recently 'dingdong.py'; then
  echo "Restarting dingdong"
  sudo systemctl stop dingdong
  sudo systemctl start dingdong
fi

if updated_recently 'telegram_bot.py'; then
  echo "Restarting bot"
  sudo systemctl stop bot
  sudo systemctl start bot
fi