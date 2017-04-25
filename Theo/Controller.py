# This is supposed to be a prototype for the different kinds of Controlleres i.e. AI bot, Learner Bot, or Human Controller
# Will probably move the functions directly affecting game state to game.py
class Controller:
	def __init__(self, player):
		self.player = player
		

	# called on player's turn 
	def TakeTurn(self):
		action = DecideAction()
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
	def DecideAction(self):
		return

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