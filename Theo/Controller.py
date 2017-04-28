# This is supposed to be a prototype for the different kinds of Controlleres i.e. AI bot, Learner Bot, or Human Controller
class Action:
	def __init__(self, n, ib, ic, it, c=0, bb=None,ac=None):
		self.name = n
		self.target = None
		self.doer = None
		self.isBlockable = ib
		self.isChallengeable = ic
		self.isTargetable = it
		self.associatedCard = ac
		self.blockableBy = bb
		self.cost = c

actions = [
			Action('Income', False, False, False),
			Action('Foreign Aid', True, False, False, 0, ['Duke']),
			Action('Tax', False, True, False, None, 0, 'Duke'),
			Action('Assassinate', True, True, True, 3,['Contessa'], 'Assassin'),
			Action('Steal', True, True, True,0,['Captain','Ambassador'], 'Captain'),
			Action('Exchange', False, True, False,0, None,'Ambassador'),
			Action('Coup', False, False, True,7)
			]

class Controller:
	def __init__(self, player, state=None):
		self.player = player
		self.state = state
		

	# called on player's turn 
	def TakeTurn(self, state):
		availableActions = self.DetermineAvailableActions()
		
		action = self.DecideAction(state,availableActions)
		
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
	def DecideAction(self, state, availableActions):
		# Query user for action
		
		# Display Board State
		DisplayBoardState(state, self.player)
		action = DisplayOptions('\nThe available actions are:',availableActions,True)
		action.doer = self.player

		# If the action has a target, get it
		if action.isTargetable:
			action.target = DisplayOptions('\nAvailable Targets',state.players,True,[self.player]+self.state.deadPlayers)

		return action

	def DetermineAvailableActions(self):		
		#must coup above 10 coins
		if self.player.cash >= 10:
			return [actions[6]]

		#else return all actions that self can afford
		availableActions = []
		for each in actions:
			if self.player.cash >= each.cost:
				availableActions.append(each)
		return availableActions




	def DecideCardToFlip(self):
		p = self.player.name+', Flip a Card!'
		return DisplayOptions(p,self.player.hand,True,self.player.deadCards)

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
				state.RevealCard(challenger, temp)
				state.ShuffleIntoDeck(self.player, [card])
				state.Draw(self.player, 1)
										
				return True
		
		#player was lying -- Action unsuccessful
		print challenger.name, ' correctly challenged ', self.player.name, ' !!!\n'
		temp = self.player.handler.DecideCardToFlip()
		state.RevealCard(self.player, temp)
		return False		

	def DecideToChallengeBlock(self, action, blocker, card):
		p= blocker.name, ' wants to block', action.doer.name,"'s ", action.name, ' with ', card
		responses = ["Allow", "Challenge"]
		
		if DisplayOptions(p,responses,False) == 'Challenge':
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

		p= 'How do you want to respond ' + self.player.name + ' ??'
		#print '******'
		response = DisplayOptions(p,responses, False)
		if response == 'Block':			
			response = DisplayOptions("Block With?",action.blockableBy,False)

		return response

	# Player selects cards to put back into deck after exchanging
	def DecideCardsToKeep(self):
		
		card1 = DisplayOptions('Choose A Card to Get rid of', self.player.hand,True, self.player.deadCards)
		 
		card2 = DisplayOptions('Choose Another Card to Get rid of',self.player.hand,True,self.player.deadCards+[card1])
		
		return [card1,card2]


# isObj = true if object array
def DisplayOptions(prompt,array, isObj, elementsToExclude=[]):
	count = 0
	indicesPrinted=[]
	print prompt
	for each in array:		
		count +=1
		if each not in elementsToExclude:			
			if isObj:
				print count, ' ', each.name
			else:
				print count, ' ', each
			indicesPrinted.append(count)
		

	index = ReadIntInput('Choose a Number\n', indicesPrinted)
	return array[index-1]

def DisplayBoardState(state, current):
	#print '\nBank = ', state.bank.cash
	PrintCoins(state.bank.cash,10)
	for each in state.players:
		print '\n ', each.name
		print '********'
		for card in each.hand:
			if card.dead:
				print card.name, ' *DEAD*'
			elif each == current:
				print card.name, ' -- ?'
			else:
				print '?'

		PrintCoins(each.cash,5)
	return

def ReadIntInput(output, possibleInputs):
	while True:
		try:
			ret = int(raw_input(output))
			if ret in possibleInputs:
				return ret
			else:
				print 'Please Choose a Valid Number'

		except ValueError:
			print 'Please Enter a Number -- Try Again'

def PrintCoins(num,delim):
	s=''
	for i in range(num):
		if i != 0 and i % delim == 0:
			s+='\n'
		s +='o'
		
	print s

	return
