import RPi.GPIO as GPIO
import dht11
import time
import datetime
import lcddriver
import Keypad
import threading
import json, requests
# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = lcddriver.lcd()
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
instance =dht11.DHT11(pin=13)
units = 'metric'
cityid = '3099434'
key = '08af92036b1f1a81bf5e4cb408e95114'
bruh = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=6cd25e0aee6543bca05f97177548320a'
spacer = " " * 16

class Thrd(threading.Thread):
	global state

	def __init__(self,idd,sleep_interval=1):
		super().__init__()
		self._kill = threading.Event()
		self._interval = sleep_interval
		self._id = idd
		
	def run(self):
		print("odpalilo sie?",self._id)
		if (self._id == 10):
			while(True):
				display.lcd_clear()
				display.lcd_display_string("Witam",1)
				is_killed = self._kill.wait(self._interval)
				if is_killed:
					break
		if (self._id == 'A'):
			H = 24
			M = 61
			S = 61
			display.lcd_clear()
			while(True):
				dt = datetime.datetime.now()
				h = dt.strftime("%H:")
				m = dt.strftime("%M:")
				s = dt.strftime("%S")
				if (h != H and m != M and s != S):
					display.lcd_display_stringg(h, 1,4)
					display.lcd_display_stringg(m, 1,7)
					display.lcd_display_stringg(s, 1,10)
				elif (m != M and s != S):
					display.lcd_display_stringg(m, 1,7)
					display.lcd_display_stringg(s, 1,10)
				elif (s != S):
					display.lcd_display_stringg(s, 1,10)
				H = h
				M = m
				S = s
				is_killed = self._kill.wait(self._interval)
				if is_killed:
					break
		if (self._id == 'B'):
			while(True):
				result = instance.read()
				if result.is_valid():
					display.lcd_clear()
					display.lcd_display_string("Temp: %-3.1f C" % result.temperature, 1)
					display.lcd_display_string("Humidity: %-3.1f %%" % result.humidity, 2)
				is_killed = self._kill.wait(self._interval)
				if is_killed:
					break
		if (self._id == 'C'):
			display.lcd_clear()
			display.lcd_display_string("Ladowanie danych", 1)
			url = requests.get(bruh)
			news = json.loads(url.text)
			wiadomosci = ['','','','','','']
			for i in range(0,6):
				wiadomosci[i] = news['articles'][i]['title']
			for i in range(0,6):
				text = spacer + wiadomosci[i]
				for j in range(0,len(text),4):
					lcd_text = text[j:(j+16)]
					display.lcd_display_string(lcd_text,1)
					time.sleep(0.1)
					display.lcd_display_string(spacer,1)	
			self.kill()
		if (self._id == 'D'):
			display.lcd_clear()
			display.lcd_display_string("Ladowanie danych", 1)
			url = requests.get('http://api.openweathermap.org/data/2.5/weather?id='+cityid+'&units='+units+'&APPID='+key)
			weather = json.loads(url.text)
			temp = weather['main']['temp']
			tempodcz = weather['main']['feels_like']
			opis = weather['weather'][0]['description']
			display.lcd_clear()
			display.lcd_display_string("Temp: %s C" % temp, 1)
			display.lcd_display_string("Odcz: %s C" % tempodcz, 2)
			time.sleep(4)
			display.lcd_clear()
			display.lcd_display_string(opis, 1)
			time.sleep(3)
			self.kill()
			
	def kill(self):
		self._kill.set()
			  
