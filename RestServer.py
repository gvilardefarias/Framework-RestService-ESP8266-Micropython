import lwip
import gc
import network
from machine import Pin
import ujson

class Response:
	def __init__(self):
		gc.collect()
		self.dat = None

		self.codes = {
			200:'ok',
			404:'not_found'
		}

	def code(self, cd):
		self.code = cd

	def contentType(self, cType):
		self.contentType = cType

	def data(self, d):
		self.dat = d
		self.contentLength = len(d.encode())

	def build(self):
		response = ""
		response += "HTTP/1.1 " + str(self.code) + " " + self.codes[self.code] + "\r\n"
		response += "Date: Mon, 27 Jul 2015 12:28:53 GMT\r\n"
		response += "Server: Simple-Python-HTTP-Server\r\n"
		response += "Last-Modified: Wed, 22 Jul 2015 19:15:56 GMT\r\n"

		if self.dat!=None:			
			response += "Content-Length: " + str(self.contentLength) + "\r\n"
			response += "Content-Type: " + self.contentType + "\r\n"

		response += "Connection: Closed\r\n"
		
		if self.dat!=None:
			response += "\r\n"
			response += self.dat + "\r\n"

		gc.collect()

		return response

class Server():
	def __init__(self, door):
		self.srv = lwip.socket()
		self.srv.bind(("", door))
		self.srv.listen(0)

	def accept(self):
		gc.collect()
		aux = self.srv.accept()
		self.cli = aux[0]
		self.addr = aux[1]

	def read(self):
		return self.cli.recv(1024)

	def send(self, data):
		self.cli.send(data.encode())

	def close(self):
		gc.collect()
		self.cli.close()

	def getPath(self, data):
		data = data.split()
		return data[1].decode()

	def start(self, paths):
		try:
			while True:
				gc.collect()
				self.accept()

				received = self.read()
				path = self.getPath(received)

				try:
					retur = paths[path]()
				except:
					response = Response()
					response.code(404)
					retur = response.build()

				self.send(retur)

				self.close()
		except:
			self.srv.close()
			return "Fail"

def POST(data, path, host, porta):
	requisicao = "POST " + path + " HTTP/1.0" + "\r\n" + "Host: " + host + "\r\n" + "User-Agent: ESP" + "\r\n" + "Accept: application/json" + "\r\n" + "If-modified-since: Sat, 29 Oct 1999 19:43:31 GMT" + "\r\n" + "Content-Type: application/json" + "\r\n" + "Content-Length: " + str(len(data)) + "\r\n" + "Connection: keep-alive" + "\r\n" + "\r\n" + data

	addr = lwip.getaddrinfo(host, porta)
	s = lwip.socket()
	s.connect(addr[0][-1])
	s.send(requisicao.encode())
	data = s.recv(1000)
	s.close()

	return data
