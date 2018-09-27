import radio
import microbit *

radio.on()
while True:
	if button_a.was_pressed()==True:
		break

while True:
	incoming = radio.receive()
	if incoming != None:
		print(incoming)
