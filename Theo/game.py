from random import shuffle
import Controller

characters = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']
actions = ['Income', 'Foreign Aid', 'Coup', 'Tax', 'Assassinate', 'Exchange', 'Steal']
counteractions = ['Block Foreign Aid', 'Block Stealing', 'Block Assassination']


class State:
	def __init__(self):
		self.players = []
		self.deck = []
		self.bank = 50

	def StartMenu(self):
		number = raw_input('Enter number of players\n')	
		return int(number)

	def initializeGame(self, numPlayers):
		
		# Add numPlayers players
		for i in range(numPlayers):
			self.players.append(Player())

		# starting money 
		for player in self.players:
			player.cash = 2
			self.bank = self.bank - 2


		# Add 3 of each card to deck, and then shuffle
		for character in characters:
			for i in range(3):
				self.deck.append(Card(character = character))

		shuffle(self.deck)

		# Fill each players hand with 2 cards from the deck
		for player in self.players:
			player.cards.append(self.deck.pop())
			player.cards.append(self.deck.pop())

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
		numPlayers = self.StartMenu()
		self.initializeGame(numPlayers)
		while not self.GameOver():
			for player in self.players:
				if not player.influence:
					continue
				else:
					#player.handler.TakeTurn()
					continue
		print "Game Over"




class Player:
	def __init__(self):
		self.name = None
		self.type = None
		self.cards = []
		self.cash = 0
		self.influence = 2
		self.handler = Controller.Controller(self)

	#def takeAction(target):

class Card:
	def __init__(self, character = None):
		self.character = None
		self.revealed = False


#called at run-time
def main():
	state = State()
	state.run()
	return


if __name__=="__main__":
	main()