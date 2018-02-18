import random

SUITS = ["ORO","ESPADA","COPA","BASTO"]

class Card(object):
	
	def __init__(self,suit,value):
		self.suit = suit
		self.value = value
		if value in (10,11,12):
			self.point = 0
		else:
			self.point = value

class Deck(object):
	def __init__(self):
		self.cards = []
		self.build()
	
	def build(self):
		for s in SUITS:
			for v in range(1,13):
				if v not in (8,9):
					self.cards.append(Card(s,v))
	
	def shuffle(self):
		for i in range(len(self.cards)-1,0,-1):
			r = random.randint(0,i)
			self.cards[i],self.cards[r]=self.cards[r],self.cards[i]
		
	def drawCard(self):
		return self.cards.pop()
		

class Player(object):
	def __init__(self,name,dealer=False):
		self.hand = []
		self.name = name
		self.points = 0
		self.dealer = dealer
		
	def draw(self,deck):
		self.hand.append(deck.drawCard())
		return self
		
	def getHand(self):
		points = 0
		data = {
			'username':self.name,
			'cards':[]
		}
		count = 0 #contar figuras
		for card in self.hand:
			data['cards'].append({
			'card':'%s de %s'%(card.value,card.suit)
			})

			points += card.point
			if card.point == 0:
				count += 1
		points %= 10 
		if count == 3:
			points = 8.5
		self.points = points
		data.update({'points':points})
		return data

class Game(object):
	
	def __init__(self):
		self.players = []
		self.dealer = None
		self.status = 0
	
	def addPlayer(self,name,dealer=False):
		if not name: return
		exists = False
		if dealer:
			for player in self.players:
				if player.dealer == True:
					print "ya existe un dealer"
					exists = True
		if not exists:
			self.players.append(Player(name,dealer))

	def playerDraw(self,name):
		for player in self.players:
			if player.name == name:
				player.draw(self.deck)
				
	def play(self):
		self.status = 1
		self.dealer = self.getDealer()
		if self.dealer is None:
			print "No se puede jugar sin dealer"
			return 
			
		self.deck = Deck()
		self.deck.shuffle()
		for player in self.players:		
			player.draw(self.deck).draw(self.deck)
			
	def getPlayer(self,name):
		for player in self.players:	
			if player.name == name:
				return player
		return None
		
	
	def getPlayerHand(self,name):
		player = self.getPlayer(name)
		return player.getHand()
		
	def getDealer(self):
		for player in self.players:	
			if player.dealer == True:
				return player
		return None
	
	def getPlayerResult(self,player):
		result = ""
		if player.points > self.dealer.points:
			result = "Ganaste!"
		elif player.points < self.dealer.points:
			result = "Perdiste!"
		else:
			result = "Empataste!"
		return result		
		
	def result(self):
		if self.dealer is None:
			print "No se puede jugar sin dealer"
			return
		data = {
			'dealer':self.getPlayerHand(self.getDealer().name),
			'players':[]
		}
		for player in self.players:
			if player != self.dealer:
				aux = {
					'hand':self.getPlayerHand(player.name),
					'name':player.name,
					'message':self.getPlayerResult(player)
				}
				data['players'].append(aux)
		self.status = 0
		return data
			
			
	
	
