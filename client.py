import socket
import json
import os

INIT = 0
WANT = 1
NOWANT = 2
RESTART = 3
FINISH = 4

class Usuario(object):
	
	def __init__(self,username):
		self.username = username
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect(('0.0.0.0', 9999))
		self.action = INIT
	
	def play(self):
		rounds = 1
		close = False
		while not close:		
			data = {
					'username': self.username,
					'action': self.action
				}
			print "Iniciando ronda (%s)..."%rounds
			
			self.client.send(json.dumps(data))
			
			#RETORNA MANO
			response = json.loads(self.client.recv(4096))
			
			for card in response['hand']['cards']:
				print "carta: ",card['card']
			print "puntos: ",response['hand']['points'],"\n\n"
			
			want = raw_input("Carta? (S/N):")
			data.update({'action':(NOWANT if want == "N" else WANT)})
			self.client.send(json.dumps(data))
			self.action = FINISH
			
			#RESULTADO
			response = json.loads(self.client.recv(4096))
			for data in response['players']:
				if data["name"] == self.username:
					print "Resultado: %s; puntos: %s"%(data["message"],data['hand']['points'])
					for card in data['hand']['cards']:
						print "carta: ",card['card']
					print "\n"
					
			print "###Dealer###"
			print "Puntos: %s"%(response["dealer"]["points"])
			for card in response['dealer']['cards']:
				print "carta: ",card['card']
			print "\n"			
			
			want = raw_input("Volver a jugar?: (S/N)")
			self.action = FINISH if want == "N" else RESTART
			if self.action == RESTART:
				data.update({'action':self.action})
				self.client.send(json.dumps(data))
				self.action = INIT
				os.system('clear')
				rounds +=1 
			else:
				print "Gracias por jugar..."
				break
				
if __name__ == "__main__":
	user = Usuario(raw_input("Ingrese su nombre de usuario:"))
	user.play()
