'''
AI controller
'''
import Controller
import random
import UI

class BotController(Controller.Controller):
	def __init__(self, player, state):
		Controller.Controller.__init__(self, player, state)
		self.tree = None
		self.vector = None

	# Returns action object, given available actions
	def ChooseAction(self, availableActions):
		#self.player.hand.sort()
		key = []
		for card in self.player.hand:
			if not card.dead:
				key.append(card.name)
		key.sort()
		key = tuple(key)
		dictionary = self.tree['Act'][key]
		action_name = RandomChoice(dictionary, self.vector, availableActions)

		action = Controller.actions[action_name]
		action.doer = self.player
		if action.isTargetable:
			target = [ player for player in self.state.players if player is not self.player][0]
			action.target = target

		return action




	# BOT decides whether to counter action.
	# Returns Allow, Challenge, or [Card] to block with
	# Always blocks with a card that can block
	def DecideToCounterAction(self, action):
		if action.name == 'Coup' or action.name == 'Income':
			return 'Allow'

		if action.isBlockable:
			for card in self.player.hand:
				if not card.dead and card.name in action.blockableBy:
					return card.name

		dictionary = self.tree['Respond'][action.name]
		counter = RandomChoice(dictionary, self.vector, dictionary.keys())

		return counter

	# Returns True if 
	def DecideToChallengeBlock(self, action, blocker, card):
		dictionary = self.tree['Respond']['Block'][(action.name, card)]
		response = RandomChoice(dictionary, self.vector, dictionary.keys())
		return response == 'Challenge'

	# BOT selects cards to put back into deck after exchanging
	# Start with 3/4 cards, put 2 back into deck
	# Returns [cards] to throw away
	def DecideCardsToKeep(self):
		cards = [card.name for card in self.player.hand if not card.dead]
		dictionary = self.tree['Exchange Cards']['Cards']

		card = RandomChoice(dictionary, self.vector, cards)
		cards.remove(card)
		if self.player.influence == 2:
			keep_same = True
			if card in cards:
				roll = random.randint(1,100)
				keep_same = roll < self.tree['Exchange Cards']['Same?']
			
			if not keep_same:
				card2 = RandomChoice(dictionary, self.vector, [card1 for card1 in cards if card1 is not card])
			else:
				card2 = RandomChoice(dictionary, self.vector, cards)
			cards.remove(card2)

		ret = []
		for card in self.player.hand:
			if card.name in cards:
				ret.append(card)
				cards.remove(card.name)

		return ret

	# Returns card to flip
	def DecideCardToFlip(self):
		if self.player.influence == 1 or self.player.hand[0].name == self.player.hand[1].name:
			if self.player.hand[0].dead:
				return self.player.hand[1]
			return self.player.hand[0]

		dictionary = self.tree['Flip Cards']
		keys = [card.name for card in self.player.hand]

		card_name = RandomChoice(dictionary, self.vector, keys)

		for card in self.player.hand:
			if card.name == card_name:
				return card

		return "ERROR"



# Given a dictionary of key:probability's, roll a random option based on probability
# Returns the key name of the chosen option
def RandomChoice(dictionary, vector, availableKeys):
	total_prob = 0
	
	for key in availableKeys:
		total_prob += vector[dictionary[key]]

	roll = random.randint(1, total_prob)

	current_max = 0
	for key in availableKeys:
		current_max += vector[dictionary[key]]
		if roll <= current_max:
			return key