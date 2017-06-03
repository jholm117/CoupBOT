import Controller
cards = ['Duke', 'Assassin', 'Ambassador', 'Captain', 'Contessa']

def ActionDecisionary(dictionary,index):	
	ad = dictionary['Act'] = {}
	cards.sort()
	i=index
	for cardIndex in range(len(cards)):
		# 2 Card hands
		for cardIndex2 in range(cardIndex, len(cards)):
			hand = (cards[cardIndex], cards[cardIndex2])

			ad[hand] = {}
			for action in Controller.actions.keys():
				ad[hand][action] = i
				i += 1
		# 1 card hands
		hand = (cards[cardIndex],)
		ad[hand] = {}
		for action in Controller.actions.keys():
			ad[hand][action] = i
			i += 1
	return i

def ExchangeDecisionary(dictionary,index):
	ed = dictionary['Exchange Cards'] = {'Cards':{},
											'Same?':index}

	index +=1
	
	for card in cards:
		ed['Cards'][card] = index
		index += 1
	return index

def ResponseDecisionary(dictionary,index):
	rd = dictionary['Respond'] = {}
	rd['Block'] = 	{
								('Foreign Aid','Duke'): {},
								('Steal','Ambassador') : {},
								('Steal', 'Captain') : {},
								('Assassinate', 'Contessa') : {}
							}
	for block in rd['Block']:
		rd['Block'][block]['Allow'] = index
		index += 1
		rd['Block'][block]['Challenge'] = index
		index += 1

	for actionKey in Controller.actions:
		if actionKey is 'Coup' or actionKey is 'Income':
			continue
		rd[actionKey] = {}
		rd[actionKey]['Allow'] = index
		index += 1

		if Controller.actions[actionKey].isBlockable:
			for card in Controller.actions[actionKey].blockableBy:
				rd[actionKey][card] = index
				index +=1
		if Controller.actions[actionKey].isChallengeable:
			rd[actionKey]['Challenge'] = index
			index += 1


	return index

def FlipCardsDecisionary(dictionary,index):
	fd = dictionary['Flip Cards'] = {}
	for card in cards:
		fd[card] = index
		index +=1
	return index


def MakeDD(dd):
	
	index = ActionDecisionary(dd,0)	
	
	index = ExchangeDecisionary(dd,index)
	
	index = ResponseDecisionary(dd,index)
	index = FlipCardsDecisionary(dd,index)
	
	return index

def printDD(dd,num):
	RecursivePrint(dd,0)
	print "\n\n\nNumber of p's = " + str(num + 1)

def RecursivePrint(dictionary,numIndent):
	indent = '\t' * numIndent
	for key in dictionary:		
		value = dictionary[key]
		if type(value) is dict:
			print indent + str(key)	
			RecursivePrint(value,numIndent+1)
		else:
			print indent + str(key) + ' ' +  str(value)

	#called at run-time

def main():
	dd = {}
	num = makeDD(dd)
	printDD(dd,num)

if __name__=="__main__":
	main()
