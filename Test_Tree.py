class Node:
	def __init__(self,probability):
		self.children = []
		self. action = None

	def add_child(self, obj, prob):
		self.children.append((obj, prob))

neutrality = Node(0)
neutral = Node(0)

income = Node(0)
foreign_aid = Node(0)

#relationships
neutrality.add_child(neutral, 1)
neutral.add_child(income, 1)
netural.add_child(foreign_aid, 1)

#actions
income.action = 'Income'
foreign_aid.action = 'Foreign Aid'