import data
delineation = []

def ActionDecisionary(dictionary,index):	
	ad = dictionary['Act'] = {}
	cardNames = data.cards
	cardNames.sort()
	index
	for cardIndex in range(len(cardNames)):
		# 2 Card hands
		for cardIndex2 in range(cardIndex, len(cardNames)):
			hand = (cardNames[cardIndex], cardNames[cardIndex2])

			rangeStart = index 
			ad[hand] = {}
			for action in data.actions.keys():
				ad[hand][action] = index
				index += 1
			delineation.append((rangeStart,index-1))

		# 1 card hands
		rangeStart = index
		hand = (cardNames[cardIndex],)
		ad[hand] = {}
		for action in data.actions.keys():
			ad[hand][action] = index
			index += 1
		delineation.append((rangeStart,index-1))
	return index

def ExchangeDecisionary(dictionary,index):
	ed = dictionary['Exchange Cards'] = {'Cards':{},
											'Same?':index}
	delineation.append((index,index))
	index +=1

	rangeStart = index
	for card in data.cards:
		ed['Cards'][card] = index
		index += 1
	delineation.append((rangeStart,index-1))
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
		delineation.append((index,index+1))
		rd['Block'][block]['Allow'] = index
		index += 1
		rd['Block'][block]['Challenge'] = index
		index += 1

	for actionKey in data.actions:
		if actionKey is 'Coup' or actionKey is 'Income':
			continue
		rangeStart = index
		rd[actionKey] = {}

		rd[actionKey]['Allow'] = index
		index += 1

		if data.actions[actionKey].isBlockable:
			for card in data.actions[actionKey].blockableBy:
				rd[actionKey][card] = index
				index +=1
		if data.actions[actionKey].isChallengeable:
			rd[actionKey]['Challenge'] = index
			index += 1
		delineation.append((rangeStart,index-1))


	return index

def FlipCardsDecisionary(dictionary,index):
	fd = dictionary['Flip Cards'] = {}
	rangeStart = index
	for card in data.cards:
		fd[card] = index
		index +=1
	delineation.append((rangeStart,index-1))
	return index


def MakeDD(dd):
	index = ActionDecisionary(dd,0)	
	index = ExchangeDecisionary(dd,index)
	index = ResponseDecisionary(dd,index)
	index = FlipCardsDecisionary(dd,index)
	
	return index


def printDD(dd,num):
	RecursivePrint(dd,0)
	print "\n\n\nNumber of p's = " + str(num)

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
	num = MakeDD(dd)
	printDD(dd,num)
	print delineation

if __name__=="__main__":
	main()