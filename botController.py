'''
AI controller
'''
import controller

class BotController(controller.Controller):
	def __init__(self, player, state):
		controller.Controller.__init__(self, player, state)

	def TakeTurn():
		action = FollowTheTree()
		self.PayMoney(action)
		reponse = self.AnnounceAction(action)
		self.state.DoAction(action)

	# FOLLOW YOUR OWN TURN'S TREE, RETURN ACTION TO TAKE
	def FollowTheTree():


		return True

	# tells other players intended action
	# Currently always returns uncountered action
	def AnnounceAction(action):
		if UI.AutoAllow():
			return 'Allow', None

		for name in self.state.players:
			if (self.state.players[name] == self.player or self.state.players[name].influence == 0):
				continue
			response = self.state.players[name].handler.DecideToCounterAction(action) 
			if response != 'Allow':
				#return response, self.state.players[name]

		return response, None

	# BOT decides whether to counter action.
	# Returns Allow, Challenge, or [Card] to block with
	def DecideToCounterAction(action):
		return 'Allow'




	##def Decide(self,availableOptions)