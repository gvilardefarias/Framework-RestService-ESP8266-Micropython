import RestServer
import network
from machine import Pin

p = Pin(0, Pin.OUT)

def on():
	p.high()
	response = RestServer.Response()
	response.code(200)
	response.contentType("text/plain")
	response.data("Ligado")
	return response.build()
def off():
	p.low()
	response = RestServer.Response()
	response.code(200)
	response.contentType("text/plain")
	response.data("Desligado")
	return response.build()

paths = {"/on":on,
	 "/off":off}

p.high()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('essid', 'password')

while not wlan.isconnected():
	pass
	
p.low()

server = RestServer.Server(8080)
server.start(paths)
