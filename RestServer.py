import lwip
import gc

class Response:
	
	def __init__(self):
		self.dat = None
		self.authorized = True

		self.codes = {
			200:'ok',
			401:'unauthorized',
			404:'not_found'
		}

	def code(self, cd):
		self.code = cd

	def contentType(self, cType):
		self.contentType = cType

	def data(self, d):
		self.dat = d
		self.contentLength = len(d.encode())

	def notAuthorized(self):
		self.code = 401
		self.authorized = False

	def build(self):
		gc.collect()
		response = ""
		response += "HTTP/1.1 " + str(self.code) + " " + self.codes[self.code] + "\r\n"
		response += "Date: Mon, 27 Jul 2015 12:28:53 GMT\r\n"
		response += "Server: Simple-Python-HTTP-Server\r\n"
		response += "Last-Modified: Wed, 22 Jul 2015 19:15:56 GMT\r\n"
		
		if not self.authorized:
			response += "WWW-Authenticate: Basic realm=\"WallyWorld\"\r\n"

		if self.dat!=None:			
			response += "Content-Length: " + str(self.contentLength) + "\r\n"
			response += "Content-Type: " + self.contentType + "\r\n"

		response += "Connection: Closed\r\n"
		
		if self.dat!=None:
			response += "\r\n"
			response += self.dat + "\r\n"

		return response

class Server():

	def __init__(self, door):
		self.authV = None
		self.srv = lwip.socket()
		self.srv.bind(("", door))
		self.srv.listen(0)

	def accept(self):
		aux = self.srv.accept()
		self.cli = aux[0]
		self.addr = aux[1]

	def read(self):
		return self.cli.read(1024)

	def send(self, data):
		self.cli.send(data.encode())

	def close(self):
		self.cli.close()

	def getPath(self, data):
		data = data.split()
		return data[1].decode()

	def auth(self, a):
		self.authV = a

	def authorized(self, da):
		if self.authV==None:
			return True

		ind = 0
		find = False
		aux = da.decode()
		aux = aux.split()

		for i in aux:
			if i=="Authorization:":
				find = True
				break
			ind += 1

		if not find:
			return False

		if (aux[ind+2])==self.authV:
			return True
		return False

	def start(self, paths):
		try:
			while True:
				gc.collect()
				self.accept()

				received = self.read()
				path = self.getPath(received)

				if self.authorized(received):
					try:
						retur = paths[path]()
					except:
						response = Response()
						response.code(404)
						retur = response.build()
				else:
					response = Response()
					response.notAuthorized()
					retur = response.build()

				self.send(retur)

				self.close()
		except:
			return "Fail"
