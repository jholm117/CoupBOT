# This is supposed to be a prototype for the different kinds of Controlleres i.e. AI bot, Learner Bot, or Human Controller
# Will probably move the functions directly affecting game state to game.py
class Action:
	def __init__(self, n, ib, ic, it, bb=None,ac=None):
		self.name = n
		self.target = None
		self.doer = None
		self.isBlockable = ib
		self.isChallengeable = ic
		self.isTargetable = it
		self.associatedCard = ac
		self.blockableBy = bb

characters = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']
actions = [
			Action('Income', False, False, False),
			Action('Foreign Aid', True, False, False, ['Duke']),
			Action('Coup', False, False, True),
			Action('Tax', False, True, False, None, 'Duke'),
			Action('Assassinate', True, True, True, ['Contessa'], 'Assassin'),
			Action('Exchange', False, True, False, None,'Ambassador'),
			Action('Steal', True, True, True,['Captain','Ambassador'], 'Captain')
			]

class Controller:
	def __init__(self, player):
		self.player = player
		

	# called on player's turn 
	def TakeTurn(self, state):
		action = self.DecideAction(state)
		
		response = self.AnnounceAction(action, state.players)
		

		if (response[0] == 'Challenge'):
			#if you do have the card in your hand
			self.RespondToChallenge(action.associatedCard,response[1],state)

		

		elif(response[0] == 'Allow'):
			state.DoAction(action)
			
		# blocked -- response = card,blocker
		elif not self.AnnounceBlock(state,action,response[0],response[1]):
			state.DoAction(action)
			
		return



	#returns action
	def DecideAction(self, state):
		# Query user for action
		
		# Display Board State
		DisplayBoardState(state, self.player)

		print 'The available actions are:\n'
		action = DisplayOptions(actions,True)
		action.doer = self.player

		# If the action has a target, get it
		if action.isTargetable:
			print '\nAvailable Targets'
			action.target = DisplayOptions(state.players,True,[self.player])

		return action

	def DecideCardToFlip(self):
		print self.player.name, ', WHICH CARD TO FLIP???'
		return DisplayOptions(self.player.hand,True)

	# tells other players intended action
	def AnnounceAction(self,action,players):
		for player in players:
			if (player == self.player):
				continue
			response = player.handler.DecideToCounterAction(action) 
			if response != 'Allow':
				return response, player

		return response, None

	# returns whether Block is successful
	def AnnounceBlock(self,state,action,card, blocker):
		for player in state.players:
			if player == blocker:
				continue
			else:				
				if player.handler.DecideToChallengeBlock(action, blocker, card):
					return blocker.handler.RespondToChallenge(card, player, state)
		return True




	# Called when challenger challenges self's action -- returns True if self was not lying
	def RespondToChallenge(self, claimedCard, challenger, state):
		for card in self.player.hand:
			if claimedCard == card.name:
				#Player wasn't lying -- Action successful
				print challenger.name, ' incorrectly challenged ', self.player.name, ' !!!\n'
				temp = challenger.handler.DecideCardToFlip()
				state.challenger.RevealCard(challenger, temp)
				state.ShuffleIntoDeck(self.player, [card])
				state.Draw(self.player, 1)
										
				return True
		
		#player was lying -- Action unsuccessful
		print challenger.name, ' correctly challenged ', self.player.name, ' !!!\n'
		temp = self.player.handler.DecideCardToFlip()
		state.RevealCard(self.player, temp)
		return False		

	def DecideToChallengeBlock(self, action, blocker, card):
		print blocker.name, ' wants to block', action.doer.name,"'s ", action.name, ' with ', card
		responses = ["Allow", "Challenge"]
		
		if DisplayOptions(responses,False) == 'Challenge':
			return True
		return False
		

	# returns Allow, Challenge, or Card to block with
	def DecideToCounterAction(self,action):
		print action.doer.name, ' wants to ', action.name
		if action.target != None:
			print 'TARGET == ', action.target.name
		
		responses = ['Allow']
		if action.isBlockable:
			if not action.isTargetable or action.target == self.player:				
				responses.append('Block')
			
		if action.isChallengeable:
			responses.append('Challenge')

		print 'How do you want to respond ', self.player.name, ' ??'
		print '******'
		response = DisplayOptions(responses, False)
		if response == 'Block':
			print "Block With?"
			response = DisplayOptions(action.blockableBy,False)

		return response


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
