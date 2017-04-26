# This is supposed to be a prototype for the different kinds of Controlleres i.e. AI bot, Learner Bot, or Human Controller
# Will probably move the functions directly affecting game state to game.py

characters = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']
actions = ['Income', 'Foreign Aid', 'Coup', 'Tax', 'Assassinate', 'Exchange', 'Steal']
target_actions = ['Coup', 'Assassinate', 'Steal']
counteractions = ['Block Foreign Aid', 'Block Stealing', 'Block Assassination']

class Controller:
	def __init__(self, player):
		self.player = player
		

	# called on player's turn 
	def TakeTurn(self, state):
		action = DecideAction(state)
		AnnounceAction(action)
		response = ListenForResponses()
		
		if (response == 'challenged'):
			RespondToChallenge()
		
		elif (response == 'countered'):
			if DecideToChallenge():
				#if successful
				if Challenge():
					Act()
				else:
					DecideCardToReveal()
					RevealCard()


		elif(response == 'allowed'):
			Act(action)
		
		# this wont ever happen but w/e
		else:
			print 'unrecognized response'

		EndTurn()



	#returns action
	def DecideAction(self, state):
		# Query user for action
		action = None
		target = None
		character = None

		print 'The available actions are:\n'
		print actions
		action = raw_input('Enter the action you would like to take\n')
		# Check that action is valid
		while action not in actions:
			print 'Not a valid action'
			action = raw_input('Enter the action you would like to take\n')

		# If the action has a target, get it
		if action in target_actions:
			print 'The available targets are:\n'
			print [target for target in state.players if target != self.player.name]
			target = raw_input('Pick your target\n')
			while target not in [target for target in state.players if target != self.player.name]:
				print 'Not a valid target'
				target = raw_input('Pick your target\n')

		# If the action is coup, pick the character
		if action == 'Coup':
			print 'The available characters to Coup are:\n'
			print characters
			character = raw_input('Pick the character')
			while character not in characters:
				print 'Not a valid character'
				character = raw_input('Pick the character')

		return action, target, character

	def DecideCardToReveal(self):
		return

	def RevealCard(self):
		return
		
	# tells other players intended action
	def AnnounceAction(self,action):
		return

	# returns 'challenged', 'countered', 'allowed'
	def ListenForResponses(self):
		return

	def RespondToChallenge(self):
		return

	# returns bool
	def DecideToChallenge(self):
		return

	# returns true if successful
	def Challenge(self):
		return

	#performs action
	def Act(self,action):
		return

	#not sure what this would do 
	def EndTurn(self):
		return