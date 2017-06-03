import os
clear = lambda: os.system('cls')

def AutoAllow():
	if DisplayOptions('Auto-Allow?',['Yes','No'],False) == 'Yes':
		return True
	return False

def ReadIntInput(output, possibleInputs):
	while True:
		try:
			ret = int(raw_input(output))
			if ret in possibleInputs:
				return ret
			else:
				print 'Choose a Valid Number'

		except ValueError:
			print 'Enter a Number -- Try Again'

# state.players index : (row,column)
TableMapping = {
				0:(0,1),
				1:(0,3),
				2:(1,4),
				3:(2,3),
				4:(2,1),
				5:(1,0)
				}
ROWS = 3
COLUMNS = 5
LINES = 9	# number of lines per block


def DisplayTable(state,currentPlayer):
	#clear()
	table = [ [ [ '' for line in range(LINES) ] for col in range(COLUMNS)] for row in range(ROWS)]
	index = 0
	for player in state.players:
		row = TableMapping[index][0]
		col = TableMapping[index][1]
		block = table[row][col]		
		
		FillBlock(block,player,player==currentPlayer)

		index += 1
	AddBankToTable(table[1][2],state.bank.cash)
	#FormatTable(table)
	#print lines of table
	playerPositions = TableMapping.values()
	
	rowNum = 0
	for row in table:
		for lineNum in range(LINES):
			line = ''
			colNum = 0
			for col in row:
				#center player names
				if ((rowNum,colNum) in playerPositions):
					if lineNum == 0:
						form = GetFormat('14',True)
					elif lineNum == 1:
						pass
						#form = GetFormat('14',False,True)
				#shrink center column
				elif colNum == 2:
					form = GetFormat('10')
				#right align everything else
				else:
					form = GetFormat('14')
				
				line += form.format(col[lineNum])
				colNum+=1

			print line
		rowNum += 1

	return

def GetFormat(blockSize,isCentered=False,isFilled=False):
	form = '{:'
	if isFilled:
		form += '-'
	if isCentered:
		form += '^'
	else:
		form += '<'
	form += blockSize + '}'
	
	return form

def FillBlock(block,player,isCurrentPlayer):
	lines = []
	
	#NAME
	if isCurrentPlayer:
		lines.append('--> ' + player.name + ' <--')
	else:
		lines.append(player.name)

	# -filled dash line
	lines.append('')

	#CARDS
	for card in player.hand:
		if card.dead:
			lines.append('X '+ card.name)
		#show current player cards in hand
		elif isCurrentPlayer:
			lines.append('? '+ card.name)
		else:
			lines.append('?')

	#MONEY
	AddCoinsToList(player.cash,5,lines)


	index = 0
	for line in lines:
		block[index] = line
		index+=1
	return

def AddBankToTable(block,bank):
	lines = []
	blankLinesToAdd = (LINES - 5)/2
	for x in range(blankLinesToAdd):
		lines.append('')
	lines = AddCoinsToList(bank,10,lines)
	
	
	index=0
	for line in lines:
		block[index] = line
		index +=1

# appends lines of delim coins to array
def AddCoinsToList(coinsLeft,delim,array):
	while (coinsLeft):
		if coinsLeft >= delim:
			array.append('o' * delim)
			coinsLeft -= delim
		else:
			array.append('o' * coinsLeft)
			return array
	return array

# isObj = true if object array
def DisplayOptions(prompt,array, isObj, elementsToExclude=[]):
	count = 0
	indicesPrinted=[]
	if prompt != None:
		print prompt
	for each in array:		
		count +=1
		if each not in elementsToExclude:			
			if isObj:
				print count, ' ', each.name
			else:
				print count, ' ', each
			indicesPrinted.append(count)
		

	index = ReadIntInput('Choose a Number\n', indicesPrinted)
	return array[index-1]


def StartMenu():
	clear()
	
	print '##################################################################'
	print '		WELCOME TO THE COUP ARENA'
	print '##################################################################'
	print '\nHow many players??'
	number = ReadIntInput('Choose Between 2-6 \n',[2,3,4,5,6])
	names = []
	for i in range(number):
		s = "Enter Player " + str(i+1) + "'s Name\n"
		name = raw_input(s)
		names.append(name)
	return names

def GameOverScreen(state):
	for player in state.players:
		if player.influence >0:
			winner = player
			break
	DisplayTable(state,winner)
	print 'Game Over'
	print winner.name, " WINS !!!"
	print 
	response = DisplayOptions('Play Again?',['Yes','No'],False)
	if response =='No':
		clear()
		exit()
	return

