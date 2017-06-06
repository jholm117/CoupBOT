
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

			
cards = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']
