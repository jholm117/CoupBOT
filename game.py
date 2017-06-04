import random
#import Controller
import botController
import UI
import decisionary

characters = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']


class State:
	def __init__(self):
		self.players = []
		self.deadPlayers = []
		self.deck = []
		self.bank = Bank()

	def InitializeGame(self, names,dd,v):
		
		# Add 3 of each cards to deck, and then shuffle
		for character in characters:
			for i in range(3):
				self.deck.append(Card(character = character))

		random.shuffle(self.deck)

		# Add names players
		for name in names:
			player = Player(name,self)
			self.players.append(player)				# add to list of players
			self.ExchangeMoney(player, self.bank, 2)	# starting money
			self.Draw(player, 2) 					#  deal 2 cards to player
			player.handler.tree = dd
			player.handler.vector = v
		
		return

	# THIS IS THE INITIALIZE GAME USED IN THE GENETIC ALGORITHM
	# Takes in 2 feature vectors, assigns v1 to the first player, v2 to the second player
	def GeneticInitializeGame(self, names, dd, v1, v2):
				# Add 3 of each cards to deck, and then shuffle
		for character in characters:
			for i in range(3):
				self.deck.append(Card(character = character))

		random.shuffle(self.deck)

		# Add names players
		for name in names:
			player = Player(name,self)
			self.players.append(player)				# add to list of players
			self.ExchangeMoney(player, self.bank, 2)	# starting money
			self.Draw(player, 2) 					#  deal 2 cards to player
			player.handler.tree = dd
		
		self.players[0].handler.vector = v1
		self.players[1].handler.vector = v2
		
		return


	def CheckGameOver(self):
		# Game is not over if two players have influence
		firstPlayer = False
		for player in self.players:
			if player.influence > 0:
				if firstPlayer:
					return False
				firstPlayer = True
				#winner = player			
		
		return True


	def Run(self):		
		while True:	
			for player in self.players:
				if self.CheckGameOver():
					return
				if player.influence:									
					player.handler.TakeTurn()
		return

	# doer attempts to take amount of money from target -(could be bank or another player)
	# use for income, tax, FA, steal
	# returns true if target has enough money
	def ExchangeMoney(self, taker, giver, amount):
		if (giver.cash >= amount):
			taker.cash += amount
			giver.cash -= amount
			return True

		# debug info
		print 'Giver does not have enough money'

		return False
		
	# move card from hand to deadCards array
	def RevealCard(self, player, card):
		player.influence -= 1
		if player.influence < 1:
			self.deadPlayers.append(player.name)
			#print 'Reveal Card'
			self.ExchangeMoney(self.bank,player,player.cash)

		card.dead = True
		player.deadCards.append(card)
		#player.hand.remove(card)
		return

	# player draws number cards - called during intialization, incorrect BS calls, and Exchange
	def Draw(self,player,number):
		for x in range(number):
			player.hand.append(self.deck.pop())

	# shuffle array of cards from players hand into deck - called for exchange and incorrect BS calls
	def ShuffleIntoDeck(self, player, cards):
		
		for card in cards:
			player.hand.remove(card)
			self.deck.append(card)

		random.shuffle(self.deck)
		return

	# this may not work with the rest of the system but can be changed
	def DoAction(self, action):
		#print '\nAction = ', action.name

		if(action.name == 'Income'):
			#print 'Income'
			self.ExchangeMoney(action.doer,self.bank, 1)
		
		elif(action.name == 'Foreign Aid'):
			#print 'FA'
			self.ExchangeMoney(action.doer,self.bank, 2)
		
		elif(action.name == 'Coup'):
			for card in action.target.hand:
				if not card.dead and action.cardToCoup == card.name:
					self.RevealCard(action.target, card)
					break
		
		elif(action.name == 'Tax'):
			#print 'Tax'
			self.ExchangeMoney(action.doer, self.bank, 3)
		
		elif(action.name == 'Steal'):
			#print 'Steal'
			self.ExchangeMoney(action.doer, action.target, 2)
		
		elif(action.name == 'Exchange'):
			self.Draw(action.doer, 2)
			cardsToDrop = action.doer.handler.DecideCardsToKeep()
			self.ShuffleIntoDeck(action.doer, cardsToDrop)
		
		elif(action.name == 'Assassinate'):
			cardToReveal = action.target.handler.DecideCardToFlip()
			self.RevealCard(action.target, cardToReveal)

		
		#print action.name, ' Successful!\n'
		return


class Player:
	def __init__(self,name,state):
		self.name = name
		self.type = None
		self.hand = []
		self.deadCards = []
		self.cash = 0
		self.influence = 2
		self.handler = botController.BotController(self,state)

class Card:
	def __init__(self, character = None):
		self.name = character
		self.dead = False

class Bank:
	def __init__(self):
		self.cash = 50

def Play():
	dictionary = {}
	index = decisionary.MakeDD(dictionary)
	feature_vector = [random.randint(1,100) for i in range(index)]
	names = UI.StartMenu()
	state = State()
	state.InitializeGame(names,dictionary,feature_vector)
	state.Run()
	UI.GameOverScreen(state)
	return

def AutoRun():
	dictionary = {}
	index = decisionary.MakeDD(dictionary)
	feature_vector = [random.randint(0,100) for i in range(index)]
	names = ['Theo', 'Jeff']
	state = State()
	state.InitializeGame(names, dictionary, feature_vector)
	state.Run()
	for player in state.players:
		if player.influence >0:
			winner = player
			break
	#UI.DisplayTable(state,winner)
	#print 'Game Over'
	#print winner.name, " WINS !!!\n\n"

# THIS IS THE GAME USED IN THE GENETIC ALGORITHM
# Takes in 2 feature vectors that represent bots
# Returns 1 if vec1 wins, 0 if vec1 loses
def GeneticPlay(vec1, vec2):
	dictionary = {}
	index = decisionary.MakeDD(dictionary)
	names = ['Test','Dummy']
	state = State()
	state.GeneticInitializeGame(names, dictionary, vec1, vec2)
	state.Run()
	return 1 if state.players[0].influence > 0 else 0

#called at run-time
def main():
	i = 0
	while True:
		AutoRun()
		i += 1
		if i % 10000 is 0:
			print i#, " games played so far \n\n"


if __name__=="__main__":
	main()