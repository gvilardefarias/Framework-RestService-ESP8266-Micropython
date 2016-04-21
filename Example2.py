import RestServer
import network
from machine import Pin

p = Pin(0, Pin.OUT)

def open():
	p.high()
	response = RestServer.Response()
	response.code(200)
	response.contentType("text/plain")
	response.data("Aberto")
	return response.build()
def close():
	p.low()
	response = RestServer.Response()
	response.code(200)
	response.contentType("text/plain")
	response.data("Fechado")
	return response.build()

paths = {"/open":open,
	 "/close":close}

p.high()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Vilar', 'defarias')

while not wlan.isconnected():
	pass
	
p.low()

server = RestServer.Server(8000)
server.auth("YTpi")
server.start(paths)
