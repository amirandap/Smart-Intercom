# Smart-Intercom

This scripts will allow you to interface a raspberry pi with a traditional commax/generic intercom found in apartment buildings. It has 2 parts:

- V27.py : This is python script that monitors when your intercom is rung and notifies you via telegram, along with voice recording and CCTV image


Installation:

Telegram Server:
1. Add "Botfather" in your telegram
2. /start
3. /newbot
4. Copy your api key into v27.py line 11
5. Get your chat ID, and replace it lines 112

MQTT Server:
1. pip install pi-mqtt-gpio
2. Edit the "config.yml" to include your mqtt topics/username/password


This is my first time learning to use GitHub and the first code I'm publishing so bear with me. I know there a million better ways of doing, documenting and achieving this but it works for me any improvement or suggestions are welcome.
