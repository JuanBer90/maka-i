import socket
import threading
from makai import Game
import json
INIT = 0
WANT = 1
NOWANT = 2
FINISH = 3

class Server(object):
    bind_ip = '0.0.0.0'
    bind_port = 9999
    SERVERNAME = "SERVER"
    
    def __init__(self):
        self.game = Game()
        self.game.addPlayer(self.SERVERNAME,True)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.bind_ip, self.bind_port))
        self.server.listen(5)  # max backlog of connections
        print 'Listening on {}:{}'.format(self.bind_ip, self.bind_port)
        
    def start(self):
        client_socket = None
        salir = False
        while not salir:
            if client_socket is None:
                client_socket, address = self.server.accept()
                print 'Accepted connection from {}:{}'.format(address[0], address[1])
            else:
                request = json.loads(client_socket.recv(1024))
                print 'Received {}'.format(request)
                if request:
					if request['action'] == INIT:
						print "se repartio la carta al usuario..."
						self.game.addPlayer(request['username'])
						self.game.play()
						data = {'hand':self.game.getPlayerHand(request['username'])}
						print data['hand']
						client_socket.send(json.dumps(data))
					elif request['action'] == WANT:
						print "el usuario pidio carta.."
						self.game.playerDraw(request['username'])
						data = { 'hand':self.game.getPlayerHand(request['username'])}
						server_hand = self.game.getPlayerHand(self.SERVERNAME)
						print "Server Hand:",server_hand['cards']
						if server_hand['points'] < 6:
							 print "El server pidio carta ... "
							 self.game.playerDraw(self.SERVERNAME)
						result = self.game.result()
						print result
						client_socket.send(json.dumps(result))
					elif request['action'] == NOWANT:
						print "El usuario no pidio carta.."
						server_hand = self.game.getPlayerHand(self.SERVERNAME)
						print "Server Hand:",server_hand['cards']
						if server_hand['points'] < 6:
							 print "El server pidio carta ... "
							 self.game.playerDraw(self.SERVERNAME)
						result = self.game.result()
						print result
						client_socket.send(json.dumps(result))
					else:
						 print " nueva ronda..."
						 self.game.__init__()
						 self.game.addPlayer(self.SERVERNAME,True)
	
if __name__ == "__main__":
    server = Server()
    server.start()
