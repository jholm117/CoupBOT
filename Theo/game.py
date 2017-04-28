from random import shuffle
import Controller

characters = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']
actions = ['Income', 'Foreign Aid', 'Coup', 'Tax', 'Assassinate', 'Exchange', 'Steal']
counteractions = ['Block Foreign Aid', 'Block Stealing', 'Block Assassination']


class State:
	def __init__(self):
		self.players = []
		self.deadPlayers = []
		self.deck = []
		self.bank = Bank()

	def initializeGame(self, numPlayers):
		
		# Add 3 of each card to deck, and then shuffle
		for character in characters:
			for i in range(3):
				self.deck.append(Card(character = character))

		shuffle(self.deck)

		# Add numPlayers players
		for i in range(numPlayers):
			
			player = Player()
			s = "Enter Player " + str(i+1) + "'s Name\n"
			name = raw_input(s)

			player.name = name
			player.handler.state = self

			self.players.append(player)				# add to list of players

			self.ExchangeMoney(player, self.bank, 2)	# starting money

			self.Draw(player, 2) 					#  deal 2 cards to player
		
		return

	def GameOver(self):
		# Game is not over if two players have influence
		firstPlayer = False
		for player in self.players:
			if player.influence:
				if firstPlayer:
					return False
				firstPlayer = True
				
		return True

	def run(self):		
		while not self.GameOver():
			for player in self.players:
				if player.influence:
					print '#########################################'
					print " 	It is ", player.name, "'s turn!"					
					print '#########################################'
					player.handler.TakeTurn(self)

		print "Game Over"
	
	# doer attempts to take amount of money from target -(could be bank or another player)
	# use for income, tax, FA, steal
	# returns true if target has enough money
	def ExchangeMoney(self, taker, giver, amount):
		if (giver.cash >= amount):
			taker.cash += amount
			giver.cash -= amount
			return True

		print 'Giver does not have enough money'
		return False
		
	# move card from hand to deadCards array
	def RevealCard(self, player, card):
		player.influence -= 1
		if player.influence < 1:
			self.deadPlayers.append(player)

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

		shuffle(self.deck)
		return

	# this may not work with the rest of the system but can be changed
	def DoAction(self, action):
		#print '\nAction = ', action.name

		if(action.name == 'Income'):
			self.ExchangeMoney(action.doer,self.bank, 1)
		
		elif(action.name == 'Foreign Aid'):
			self.ExchangeMoney(action.doer,self.bank, 2)
		
		elif(action.name == 'Coup'):
			self.ExchangeMoney(self.bank, action.doer, 7)
			cardToReveal = action.target.handler.DecideCardToFlip()		# need to write this function
			self.RevealCard(action.target, cardToReveal)
		
		elif(action.name == 'Tax'):
			self.ExchangeMoney(action.doer, self.bank, 3)
		
		elif(action.name == 'Steal'):
			self.ExchangeMoney(action.doer, action.target, 2)
		
		elif(action.name == 'Exchange'):
			self.Draw(action.doer, 2)
			cardsToDrop = action.doer.handler.DecideCardsToKeep()
			self.ShuffleIntoDeck(action.doer, cardsToDrop)
		
		elif(action.name == 'Assassinate'): 
			self.ExchangeMoney(action.doer,self.bank,3)

			cardToReveal = action.target.handler.DecideCardToFlip()
			self.RevealCard(action.target, cardToReveal)

		
		print action.name, ' Successful!\n'
		return



class Player:
	def __init__(self):
		self.name = None
		self.type = None
		self.hand = []
		self.deadCards = []
		self.cash = 0
		self.influence = 2
		self.handler = Controller.Controller(self,)

class Card:
	def __init__(self, character = None):
		self.name = character
		self.dead = False

class Bank:
	def __init__(self):
		self.cash = 50


def StartMenu():
	print '##################################################################'
	print '		WELCOME TO THE COUP ARENA'
	print '##################################################################'
	print '\nHow many players??'
	number = Controller.ReadIntInput('Choose Between 2-6 \n',[2,3,4,5,6])
	return number

#called at run-time
def main():
	numPlayers = StartMenu()
	state = State()
	state.initializeGame(numPlayers)
	state.run()
	return


if __name__=="__main__":
	main()