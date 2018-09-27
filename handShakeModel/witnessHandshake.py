name="Kevin Xie"

def start():
	while accelerometer.current_gesture() != "shake":
	    pass
	else:
	    radio.send(name)
	    handshake()

def handshake():




radio.on()
radio.config(channel=0)

start()