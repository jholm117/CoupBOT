# This is supposed to be a prototype for the different kinds of Controlleres i.e. AI bot, Learner Bot, or Human Controller
# Will probably move the functions directly affecting game state to game.py

characters = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']
actions = ['Income', 'Foreign Aid', 'Coup', 'Tax', 'Assassinate', 'Exchange', 'Steal']
target_actions = ['Coup', 'Assassinate', 'Steal']
counteractions = ['Block Foreign Aid', 'Block Stealing', 'Block Assassination']
#responses = ['Allow', 'Counter', 'Challenge']

class Controller:
	def __init__(self, player):
		self.player = player
		

	# called on player's turn 
	def TakeTurn(self, state):
		action = self.DecideAction(state)
		
		response = self.AnnounceAction(action, state.players)
		print response

		if (response == 'Challenge'):
			self.RespondToChallenge()
		
		elif (response == 'Block'):
			if self.DecideToChallenge():
				#if successful
				if self.Challenge():
					state.DoAction(action);
				else:
					DecideCardToReveal()
					RevealCard()


		elif(response == 'Allow'):
			state.DoAction(action)
		
		# this wont ever happen but w/e
		else:
			print 'unrecognized response'

		#state.DoAction(action)

		#EndTurn()
		return



	#returns action
	def DecideAction(self, state):
		# Query user for action
		
		# Display Board State
		DisplayBoardState(state, self.player)

		print 'The available actions are:\n'
		action = Action(DisplayOptions(actions,False),self.player)
		
		# If the action has a target, get it
		if action.name in target_actions:
			print '\nAvailable Targets'

			action.target = DisplayOptions(state.players,True,[self.player])

		return action

	def DecideCardToFlip(self):
		print self.player.name, ' WHICH CARD TO FLIP???'
		return DisplayOptions(self.player.hand)

	def RevealCard(self):
		return
		
	# tells other players intended action
	def AnnounceAction(self,action,players):
		for player in players:
			if (player == self.player):
				continue
			response = player.handler.DecideToCounter(action) 
			if response != 'Allow':
				return response

		return response

	# returns 'challenged', 'countered', 'allowed'
	def ListenForResponses(self):
		return

	def RespondToChallenge(self):
		return

	# returns bool
	def DecideToCounter(self,action):
		print action.doer.name, ' wants to ', action.name
		if action.target != None:
			print 'TARGET == ', action.target.name
		
		responses = ['Allow']
		if action.isBlockable:
			responses.append('Block')
		if action.isChallengeable:
			responses.append('Challenge')
		
		response = DisplayOptions(responses, False)
		print response
		return response

	# returns true if successful
	def Challenge(self):
		return

	#not sure what this would do 
	def EndTurn(self):
		return

class Action:
	def __init__(self, n, d, t=None):
		self.name = n
		self.target = t
		self.doer = d
		self.isBlockable = False
		self.isChallengeable = False

# isObj = true if object array
def DisplayOptions(array, isObj, elementsToExclude=[]):
	count = 0

	for each in array:
		if each not in elementsToExclude:
			if isObj:
				print count, ' ', each.name
			else:
				print count, ' ', each
		count += 1

	index = int(raw_input('Choose a Number\n'))
	while (index < 0 or index >= count):
	 	index = int(raw_input('Invalid Number -- Try Again\n'))
	return array[index]

def DisplayBoardState(state, current):
	print 'BOARD STATE'
	for each in state.players:
		print '\n', each.name
		print '***********************'
		print 'influence = ', each.influence
		
		for card in each.deadCards:
			print card.name
		print 'money = ', each.cash

	print '\nMoney in the pot = ', state.bank.cash,'\n\n'

	print 'Cards in Hand '
	for each in current.hand:
		print each.name
	print '\n'
	return
