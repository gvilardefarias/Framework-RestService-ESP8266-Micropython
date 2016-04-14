import RestServer

def a():
	response = RestServer.Response()
	response.code(200)
	response.contentType("text/plain")
	response.data("a")
	return response.build()
def b():
	response = RestServer.Response()
	response.code(200)
	response.contentType("text/plain")
	response.data("b")
	return response.build()

paths = {"/a":a,
		 "/b":b}

server = RestServer.Server(8080)
server.start(paths)