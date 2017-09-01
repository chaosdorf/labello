#!/usr/bin/env python3
# It does work with Python 2.7, too.

from __future__ import print_function
from __future__ import unicode_literals

try:
    from SocketServer import TCPServer, BaseRequestHandler
except ImportError: # Python 3
    from socketserver import TCPServer, BaseRequestHandler

class DummyHandler(BaseRequestHandler):
    """ Simply write everything to stdout. """
    
    def handle(self):
        print("-----------------------------------------------------")
        print("New connection from {}:".format(self.client_address))
        buffer = b''
        while True:
            data = self.request.recv(1024)
            if data:
                buffer += data
            else:
                break
        print(buffer)
        print("-----------------------------------------------------")

if __name__ == "__main__":
    listen_config = ("127.0.0.1", 9100)
    print("Listening at {}...".format(listen_config))
    server = TCPServer(listen_config, DummyHandler)
    server.serve_forever()
