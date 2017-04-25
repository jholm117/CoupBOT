from random import shuffle

characters = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']
actions = ['Income', 'Foreign Aid', 'Coup', 'Tax', 'Assassinate', 'Exchange', 'Steal']
counteractions = ['Block Foreign Aid', 'Block Stealing', 'Block Assassination']


class State:
	def __init__(self):
		self.players = []
		self.deck = None

	def initializeGame():
		# Add 6 random players
		for i in range(6):
			self.players.append()

		# Add 3 of each card to deck, and then shuffle
		for character in characters:
			for i in range(3):
				deck.append(Card(character = character))

		shuffle(deck)

		# Fill each players hand with 2 cards from the deck
		for player in players:
			player.cards.append(deck.pop())
			player.cards.append(deck.pop())

	def GameOver():
		# Game is not over if two players have influence
		firstPlayer = False
		for player in players:
			if player.influence:
				if firstPlayer:
					return False
				firstPlayer = True
				
		return True

	def run():
		self.initializeGame()
		while not self.GameOver():
			for player in players:
				if not player.influence:
					continue




class Player:
	def __init__(self):
		self.name = None
		self.type = None
		self.cards = []
		self.cash = 2
		self.influence = 2

	def takeAction(target):

class Card:
	def __init__(self, character = None):
		self.character = None
		self.revealed = False