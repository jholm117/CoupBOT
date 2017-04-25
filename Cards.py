import random

# rn just asks the player to press enter to shuffle, q to quit
def PromptPlayer(deck):
	s = raw_input("Press 'Enter' to shuffle -- 'q' to Quit\n")
	if(s==''):

		print "\nShuffling..."
		ShuffleDeck(deck)
		PrintDeck(deck)

	elif (s == 'q'):
		exit()

	return

# Shuffle cards in deck
def ShuffleDeck(deck):
	random.shuffle(deck)
	return

# Display types of cards in deck
def PrintDeck(deck):
	print "deck =\n"
	for card in deck:
		print card.get_type()
	return

# Card with type field
class Card:
	def __init__(self,kind):
		self.type = kind

	def get_type(self):
		return self.type

# Player object with hand field
class Player:
	def __init__(self,hand):
		self.hand = hand

	def get_hand(self):
		return self.hand
