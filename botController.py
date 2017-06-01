'''
AI controller
'''
import Controller
import random
import UI

class BotController(Controller.Controller):
	def __init__(self, player, state):
		Controller.Controller.__init__(self, player, state)

	def TakeTurn(self):
		print UI.DisplayTable(self.state, self.player)
		action = self.FollowTheTree(self.player.tree)
		self.PayMoney(action)
		reponse = self.AnnounceAction(action)
		self.state.DoAction(action)
		#print "Player ", self.player.name, " did ", action.name, " and has ", self.player.cash, " cash"
		return

	# FOLLOW YOUR OWN TURN'S TREE, RETURN ACTION TO TAKE
	def FollowTheTree(self, root):
		# If the node has an action, it s a leaf, and you do that action
		if root.action:
			action = Controller.actions[root.action]
			action.doer = self.player
			return action
			# RETURN ACTION

		# If the root is not an action, follow its children according to probabilities
		total_prob = 0
		for child in root.children:
			total_prob += child[1]

		roll = random.randint(1,total_prob)

		current_max = 0
		for child in root.children:
			current_max += child[1]
			if roll <= current_max:
				return self.FollowTheTree(child[0])

		print "ERRRRORORO"
		return


	# tells other players intended action
	# Currently always returns uncountered action
	def AnnounceAction(self, action):
		if UI.AutoAllow():
			return 'Allow', None

		for name in self.state.players:
			if (self.state.players[name] == self.player or self.state.players[name].influence == 0):
				continue
			response = self.state.players[name].handler.DecideToCounterAction(action) 
			if response != 'Allow':
				a = 0#return response, self.state.players[name]

		return response, None

	# BOT decides whether to counter action.
	# Returns Allow, Challenge, or [Card] to block with
	def DecideToCounterAction(self, action):
		return 'Allow'




	##def Decide(self,availableOptions)