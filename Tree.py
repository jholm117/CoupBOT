
class Node:
	def __init__(self,probability):
		self.children = []
		self. action = None

	def add_child(self, obj, prob):
		self.children.append((obj, prob))

#bot's turn
neutrality = Node(0)
not_neutral = Node(0)
neutral = Node(0)

#neutral nodes
income = Node(0)
foreign_aid = Node(0)
coup = Node(0)

#not neutral nodes
lie = Node(0)
truth = Node(0)

neutrality.add_child(not_neutral, 15)
print neutrality.children

