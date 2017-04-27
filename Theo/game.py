from random import shuffle
import Controller

characters = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']
actions = ['Income', 'Foreign Aid', 'Coup', 'Tax', 'Assassinate', 'Exchange', 'Steal']
counteractions = ['Block Foreign Aid', 'Block Stealing', 'Block Assassination']


class State:
	def __init__(self):
		self.players = []
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
				if not player.influence:
					continue

				#player.handler.TakeTurn()
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
		player.deadCards.append(card)
		player.hand.remove(card)

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
	def DoAction(self, action, doer, target):
		print '\nAction = ',action

		if(action == 'Income'):
			self.ExchangeMoney(doer,self,bank, 1)
		
		elif(action == 'Foreign Aid'):
			self.ExchangeMoney(doer,self.bank, 2)
		
		elif(action == 'Coup'):
			self.ExchangeMoney(self.bank, doer, 7)
			cardToReveal = target.DecideCardToFlip()		# need to write this function
		
		elif(action == 'Tax'):
			self.ExchangeMoney(doer, self.bank, 3)
		
		elif(action == 'Steal'):
			self.ExchangeMoney(doer, target, 2)
		
		elif(action == 'Exchange'):
			self.Draw(doer, 2)

			# need to write this function
			cardsToDrop = doer.DecideCardsToKeep()
			self.ShuffleIntoDeck(doer, cardsToDrop)
		
		elif(action == 'Assassinate'): 
			self.ExchangeMoney(doer,self.bank,3)

			cardToReveal = target.DecideCardToFlip()
			RevealCard(target,cardToReveald)

		
		else:
			print 'action not recognized'
		return



class Player:
	def __init__(self):
		self.name = None
		self.type = None
		self.hand = []
		self.deadCards = []
		self.cash = 0
		self.influence = 2
		self.handler = Controller.Controller(self)

class Card:
	def __init__(self, character = None):
		self.character = character
		self.dead = False

class Bank:
	def __init__(self):
		self.cash = 50


def StartMenu():
	number = int(raw_input('Enter number of players\n'))

	while number > 6 or number < 2:
		number = int(raw_input('Choose 2-6 players\n'))

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