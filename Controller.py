# This is supposed to be a prototype for the different kinds of Controlleres i.e. AI bot, Learner Bot, or Human Controller
import UI
import game

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
		self.cardToCoup = None

actions = {
			'Income' : 		Action('Income', False, False, False),
			'Foreign Aid' : Action('Foreign Aid', True, False, False, 0, ['Duke']),
			'Tax' : 		Action('Tax', False, True, False, None, 0, 'Duke'),
			'Assassinate' : Action('Assassinate', True, True, True, 3,['Contessa'], 'Assassin'),
			'Steal' : 		Action('Steal', True, True, True,0,['Captain','Ambassador'], 'Captain'),
			'Exchange'  :	Action('Exchange', False, True, False,0, None,'Ambassador'),
			'Coup' : 		Action('Coup', False, False, True,7)
			}


class Controller:
	def __init__(self, player, state):
		self.player = player
		self.state = state
		

	# called on player's turn -- main function
	def TakeTurn(self):
		UI.DisplayTable(self.state,self.player)
		# get possible actions
		availableActions = self.DetermineAvailableActions()
		
		#choose an action
		action = self.ChooseAction(availableActions)
		print action.doer.name, " uses ", action.name

		#pay money if applicable
		self.PayMoney(action)
		
		# announce your choice to the table
		response = self.AnnounceAction(action)		

		if (response[0] == 'Challenge'):
			#if you do have the card in your hand
			if self.RespondToChallenge(action.associatedCard,response[1]):
				self.state.DoAction(action)

		

		elif(response[0] == 'Allow'):
			self.state.DoAction(action)
			
		# blocked -- response = card,blocker
		else:
			print response[1].name, " blocked with ", response[0]
			if not self.AnnounceBlock(action,response[0],response[1]):
				self.state.DoAction(action)
		

		print '\n\n'
		return

	# Returns a list of the names of available actions
	def DetermineAvailableActions(self):		
		
		#must coup above 10 coins
		if self.player.cash >= 10:
			return ['Coup']

		availableActions = []

		if self.state.bank.cash >= 1:
			availableActions.append('Income')
		if self.state.bank.cash >= 2:
			availableActions.append('Foreign Aid')
		if self.state.bank.cash >= 3:
			availableActions.append('Tax')

		for player in self.state.players:
			if player == self.player:
				continue
			if player.cash >= 2:
				availableActions.append('Steal')
				break

		availableActions.append('Exchange')

		if self.player.cash >= 3:
			availableActions.append('Assassinate')
		if self.player.cash >=7:
			availableActions.append('Coup')

		return availableActions


	# tells other players intended action -- should return if action is successful
	def AnnounceAction(self,action):
		#if UI.AutoAllow():
		#	return 'Allow', None

		for player in self.state.players:
			if (player == self.player or player.influence == 0):
				continue
			response = player.handler.DecideToCounterAction(action) 
			if response != 'Allow':
				return response, player

		return response, None

	# returns whether Block is successful
	def AnnounceBlock(self,action,card, blocker):
		#if UI.AutoAllow():
		#	return True
		for player in self.state.players:
			if player == blocker or player.influence == 0:
				continue		
			if player.handler.DecideToChallengeBlock(action, blocker, card):
				return blocker.handler.RespondToChallenge(card, player)
		return True

		#pay up
	def PayMoney(self,action):
		if action.cost > 0:
			self.state.ExchangeMoney(self.state.bank,self.player,action.cost)
		return


	# Called when challenger challenges self's action -- returns True if self was not lying
	def RespondToChallenge(self, claimedCard, challenger):
		for card in self.player.hand:
			if claimedCard == card.name and not card.dead:
				#Player wasn't lying -- Action successful
				print challenger.name, ' incorrectly challenged ', self.player.name, ' !!!\n'
				temp = challenger.handler.DecideCardToFlip()
				self.state.RevealCard(challenger, temp)
				self.state.ShuffleIntoDeck(self.player, [card])
				self.state.Draw(self.player, 1)
										
				return True
		
		#player was lying -- Action unsuccessful
		print challenger.name, ' correctly challenged ', self.player.name, ' !!!\n'
		temp = self.player.handler.DecideCardToFlip()
		self.state.RevealCard(self.player, temp)
		return False


	'''
		All Decision Functions Below

	'''
	def Decide(self, availableOptions, prompt=None):
		UI.DisplayTable(self.state,self.player)
		choice = UI.DisplayOptions(prompt, availableOptions, False)
		return choice

	#returns action -- Called when self begins turn
	def ChooseAction(self, availableActions):
		# Query user for action
		# Display Board State
		
		actionKey = self.Decide(availableActions, 'Available Actions:')
		action = actions[actionKey]
		action.doer = self.player

		# If the action has a target, get it
		if action.isTargetable:
			availableTargets = [player.name for player in self.state.players if player is not self.player]
			targetKey = self.Decide(availableTargets, 'Available Targets:')
			for player in self.state.players:
				if player.name is targetKey:
					action.target = player
					break

		#choose target's card to coup
		if actionKey == 'Coup':
			action.cardToCoup = self.Decide(game.characters,'Cards to Coup:')

		return action

	#Called when self loses influence
	def DecideCardToFlip(self):
		p = self.player.name+', Flip a Card!'
		return UI.DisplayOptions(p,self.player.hand,True,self.player.deadCards)

	# Called when blocker attempts to counter an action
	def DecideToChallengeBlock(self, action, blocker, card):
		p= blocker.name+ ' wants to block '+ action.doer.name+"'s "+ action.name+ ' with '+ card
		responses = ["Allow", "Challenge"]
		
		if self.Decide(responses,p) == 'Challenge':
			return True
		return False
		

	# returns Allow, Challenge, or Card to block with
	def DecideToCounterAction(self,action):
		UI.DisplayTable(self.state,self.player)
		p = action.doer.name+ ' wants to '+ action.name
		if action.target != None:
			p+= ' /// TARGET == '+ action.target.name
		
		responses = ['Allow']
		if action.isBlockable:
			if not action.isTargetable or action.target == self.player:				
				responses.append('Block')
			
		if action.isChallengeable:
			responses.append('Challenge')

		#p= 'How do you want to respond ' + self.player.name + ' ??'
		
		response = UI.DisplayOptions(p,responses, False)
		if response == 'Block':			
			response = UI.DisplayOptions("Block With?",action.blockableBy,False)

		return response

	# Player selects cards to put back into deck after exchanging
	def DecideCardsToKeep(self):
		UI.DisplayTable(self.state,self.player)
		card1 = UI.DisplayOptions('Get rid of One Card:', self.player.hand,True, self.player.deadCards)
		 
		card2 = UI.DisplayOptions('Get rid of Another Card:',self.player.hand,True,self.player.deadCards+[card1])
		
		return [card1,card2]


