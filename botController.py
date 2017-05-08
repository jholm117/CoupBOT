'''
AI controller


'''
import controller

ActionProbability = {
					'Income' : 			9,
					'Foreign Aid' : 	2,
					'Tax' : 			3,
					'Assassinate' : 	4,
					'Steal' : 			5,
					'Exchange' : 		6,
					'Coup' : 			7
					}

class BotController(controller.Controller):
	def __init__(self, player, state):
		controller.Controller.__init__(self, player, state)

	def Decide(self,availableOptions)