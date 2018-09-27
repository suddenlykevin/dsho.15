import radio
import random
from microbit import *

PIN = ""
enteredPIN = ""
linkCode = 0
incoming= None
radio.on()
boat1 = Image("00000:"
              "00000:"
              "00000:"
              "00000:"
              "00900")
boat2 = Image("00000:"
              "00000:"
              "00000:"
              "00900:"
              "09990")
boat3 = Image("00000:"
              "00000:"
              "00000:"
              "00800:"
              "08880")
boat4 = Image("00000:"
              "00000:"
              "00000:"
              "08780:"
              "27672")
boat5 = Image("00900:"
              "09890:"
              "88788:"
              "77677:"
              "66466")
boat6 = Image("56665:"
              "46664:"
              "46653:"
              "46664:"
              "56665")
boat6 = Image("54445:"
              "66666:"
              "66666:"
              "66566:"
              "54345")
boat9 = Image("99999:"
              "99099:"
              "90909:"
              "90009:"
              "99999")
all_boats=[boat1,boat2,boat3,boat4,boat5,boat6]

def loading():
    for b in range(10):
        for x in range(5):
    	    for y in range(5):
    	        display.set_pixel(x, y, b)
        sleep(50)
	for b in range(10):
	    for x in range(5):
	        for y in range(5):
	            display.set_pixel(x, y, 9-b)
	    sleep(50)

def pinEnter():
	global enteredPIN
	deg = 0
	t=0
	letterA=False
	letterB=False
	while deg<4:
		display.show(str(t))
		if button_a.was_pressed():
			if letterA==False and letterB==False:
				letterA=True
				t+=1
			elif letterA==True:
				if t==9:
					t=0
				else:
					t+=1
			elif letterB==True:
				enteredPIN=enteredPIN+str(t)
				letterB=False
				deg+=1
				t=0
				letterA=True
		if button_b.was_pressed():
			if letterA==False and letterB==False:
				letterB=True
				t+=1
			elif letterB==True:
				if t==9:
					t=0
				else:
					t+=1
			elif letterA==True:
				enteredPIN=enteredPIN+str(t)
				letterA=False
				deg+=1
				t=0
				letterB=True
	while button_b.was_pressed()==False:
		display.scroll(enteredPIN+"|->")
		if button_a.was_pressed()==True:
			display.show(Image.NO)
			enteredPIN=""
			pinEnter()
	if PIN=="":
		pinGenerate()
	else:
		microWait()


def pinGenerate():
	global PIN
	for x in range(4):
		PIN = PIN+str(random.randint(0,9))
	while button_b.was_pressed()==False:
		display.scroll(PIN+"|->")
		if button_a.was_pressed()==True:
			display.show(Image.NO)
			microbit.reset()
	if enteredPIN=="":
		pinEnter()
	else:
		microWait()

def microWait():
    global linkCode, PIN, enteredPIN, incoming
    if int(PIN)>int(enteredPIN):
        linkCode=int(PIN+enteredPIN)
    else:
        linkCode=int(enteredPIN+PIN)
    radio.config(channel=(linkCode%83)+1)
    handshake()
    
def handshake():
    global linkCode, incoming
    loading()
    while accelerometer.current_gesture() != "shake":
	    pass
    while incoming != str(linkCode):
        incoming = radio.receive()
        radio.send(str(linkCode))
    flash("g")
    sleep(200)
    syncShow()

def syncShow():
	global PIN, enteredPIN, incoming
	if PIN>enteredPIN:
		for x in range(5):
			display.clear()
			display.set_pixel(2,x,5)
			sleep(75)
			display.clear()
		radio.send("sync")
		sleep(400)
		while incoming != "syncverify":
			incoming = radio.receive()
		for x in range(5):
			display.clear()
			display.set_pixel(2,4-x,5)
			sleep(75)
			display.clear()
		for x in range(5):
			display.clear()
			display.set_pixel(2,x,5)
			sleep(75)
			display.clear()
		radio.send("collision")
		display.show(all_boats, delay=50)
	if PIN<enteredPIN:
		while incoming != "sync":
			incoming = radio.receive()
		for x in range(5):
			display.clear()
			display.set_pixel(2,4-x,5)
			sleep(75)
			display.clear()
		for x in range(5):
			display.clear()
			display.set_pixel(2,x,5)
			sleep(75)
			display.clear()
		radio.send("syncverify")
		sleep(400)
		while incoming != "collision":
			incoming = radio.receive()
		display.show(all_boats, delay=50)
	for b in range(6):
	    for t in range(5):
	        for y in range(5):
	            display.set_pixel(y, t, 5-b)
		    sleep(65)
	messaging()

def flash(status):
	if status == "g":
	    for x in range(3):
		    display.show(Image.YES)
		    sleep(200)
	elif status == "r":
	    for x in range(3):
		    display.show(Image.SKULL)
		    sleep(200)

def messaging():
    display.clear()
    display.show(boat9)

while True:
	if button_a.was_pressed()==True:
		pinGenerate()
	elif button_b.was_pressed()==True:
		pinEnter()
