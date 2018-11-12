#!/usr/bin/python3
import RPi.GPIO as GPIO
import subprocess
import shlex
import time, datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

now = datetime.datetime.now()
telegram_bot = telepot.Bot('597228802:AAGHvtTRo3LWoP3gI4BdddvpHxGhC5iPsYM')
bandera = "False"


def greeting():
    command_line = 'aplay --device plughw:CARD=Device,DEV=0 /home/pi/greeting.wav'
    args = shlex.split(command_line)
    subprocess.call(args)
    print("Preguntando quien es")

def answer():
	command_line = 'sudo arecord -D plughw:1 --duration=3 -f cd /home/pi/answer.wav'
	args = shlex.split(command_line)
	subprocess.call(args)
	getCurrentPicture()

	telegram_bot.sendPhoto(569563829, photo=open('/home/pi/visitante.jpg','rb'))
	telegram_bot.sendAudio(569563829, audio=open('/home/pi/answer.wav','rb'))
	
#Cuando el intercom no esta en automatico    
def telegram():
	telegram_bot.sendMessage (569563829, str("Estan tocando el intercom!!! y el automatico esta" + str(bandera)))
	telegram_bot.sendAudio(569563829, audio=open('/home/pi/answer.wav','rb'))

def action(msg):
	chat_id = msg['chat']['id']
	command = msg['text']
	global bandera
	if command == '/hi':
	   telegram_bot.sendMessage (chat_id, str("IntercomPI Funcionando"))
	elif command == 'Abrir':
		GPIO.output(11, 0)
		GPIO.output(7, 0)
		GPIO.output(13, 1)
		time.sleep(2)
		GPIO.output(13, 0)
		print("tamo abriendo")
		telegram_bot.sendMessage (chat_id, str("Abriendo intercom!!!"))
	elif command == '/on':
		bandera = "True"
		print("Automatico: " + str(bandera))
		telegram_bot.sendMessage (chat_id, str("Automatico: " + str(bandera)))
	elif command == '/off':
		bandera = "False"
		print("Automatico: " + str(bandera))
		telegram_bot.sendMessage (chat_id, str("Automatico: " + str(bandera)))
	elif command == 'Status':
		print("Automatico: " + str(bandera))
		telegram_bot.sendMessage (chat_id, str("Automatico: " + str(bandera)))
	elif command == 'Repetir':
		print("Enviando Nota de Voz")
		answer()
	elif command == '/probando':
		answer()
		print("Grabando y Enviando")
		telegram_bot.sendAudio(chat_id, audio=open('/home/pi/answer.wav','rb'))
		print("Enviado")

#lee una imagen del url de la camara de seguridad
def getCurrentPicture():
	import requests
	from requests.auth import HTTPBasicAuth

	image_url = 'http://10.0.0.246/ISAPI/Streaming/channels/0700/picture?videoResolutionWidth=1920&videoResolutionHeight=1080'
	img_data = requests.get(image_url, auth=HTTPBasicAuth('admin', 'Acropolis12')).content
	with open('/home/pi/visitante.jpg', 'wb') as handler:
	    handler.write(img_data)
	

   
def pulsador():
	if (GPIO.input(16)):
		print("Tocaron la puerta")
		GPIO.output(11, 1)
		GPIO.output(7, 1)
		time.sleep(2)
		greeting()
		print("Respondi")
		answer()
		GPIO.output(11, 0)
		GPIO.output(7, 0)
		if (bandera == "False"):
			print("Esperando telegram para abir")
			telegram()
		if (bandera == "True"):
			GPIO.output(13, 1)
			time.sleep(2)
			GPIO.output(13, 0)
			telegram_bot.sendMessage (569563829, str("Abriendo intercom!!!"))
			print("Abriendo")

        
        
if __name__ == '__main__':
    MessageLoop(telegram_bot, action).run_as_thread()
    try: 
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.IN)
        GPIO.setwarnings(False)
        GPIO.setup(7, GPIO.OUT, initial=0)   
        GPIO.setup(11, GPIO.OUT, initial=0)
        GPIO.setup(13, GPIO.OUT, initial=0)
        print("Try")
        telegram_bot.sendMessage (569563829, str("Bienvenido a Ana Paula 801A v2"), 
		reply_markup=ReplyKeyboardMarkup(
		keyboard=[[KeyboardButton(text="Abrir"), KeyboardButton(text="China"), KeyboardButton(text="Repetir")],[KeyboardButton(text="Status"), KeyboardButton(text="/on"), KeyboardButton(text="/off")]])
                                	)
        while True:
            pulsador()
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit(0)
    except Exception as e:
        print("Error durante ejecucion:")
        print(e)            
    finally:
        GPIO.cleanup()
        exit(1)