from screen import HTTPRequestHandler
from BaseHTTPServer import HTTPServer

port = 1552
ip =  'localhost'

try:
    server = HTTPServer(('', port), HTTPRequestHandler)
    print 'Started httpserver on port ' , port
   
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
   print '^C received, shutting down the web server'
   server.socket.close()