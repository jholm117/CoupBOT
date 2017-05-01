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

def PrintCoins(num,delim):
	s=''
	for i in range(num):
		if i != 0 and i % delim == 0:
			s+='\n'
		s +='o'
		
	print s

	return

def CoinStrBuilder(num,delim,row,array):
	if row != 1:
		return num
	if num <1:
		array.insert(1,'')
		return 0

	s=''
	i=0	
	for i in range(1,num):
		if (i > delim):
			i-=1
			break
		s+='o'
	num -= i
	array.insert(1,s)
	return num


#lost cause --jk
def BuildTable(state,current):
	clear()
	print '#########################################'
	print " 	It is ", current.name, "'s turn!"					
	print '#########################################'

	numPlayers = len(state.players)
	s= ''
	playersToPrint= []

	# i = 0, 1, 2
	for row in range(3): 
		index = row*2
		playersToPrint= []
		if index < numPlayers:
			playersToPrint.append(state.players[index])
			if index+1 < numPlayers:
				playersToPrint.append(state.players[index+1])
		elif row == 2:
			break
	
		array=[]
		opt = row % 2 == 0
		for each in playersToPrint:
			array += [each.name]
		
		
		coinsleft = state.bank.cash
		coinsleft = CoinStrBuilder(coinsleft,10,row,array)		
			

		print_row(array,opt)
	
		
		for k in range(2):
			array=[]
			for each in playersToPrint:
				card = each.hand[k]
				if card.dead:
					array += ['X '+ card.name] 
				elif each == current:

				 	array += ['? ' + card.name]
				else:
					array += ['?']
			coinsleft = CoinStrBuilder(coinsleft,10,row,array)
			print_row(array,opt)


		print ''
		'''
		# Cards
		for k in range(2):
			for each in playersToPrint:
				card = each.hand[k]
				if card.dead:
					s+= 'X ', card.name 
				else:
				 	s+= '? '
				 	if each == current:
				 		s += card.name
				s+='	'
			s+='\n'
		
		s+='\n'
		'''
		#for each in playersToPrint:
	return

def print_row(strArray,optionalOffset =False):
	s=''
	t=()
	if optionalOffset:
		s+="%-6s"
		t+=('',)
	for each in strArray:
		s+= "%-12s "
		t += (each,)
	print s % t
	#print " %-15s, %-15s, %15s" % (str1,str2,str3)
	return



# isObj = true if object array
def DisplayOptions(prompt,array, isObj, elementsToExclude=[]):
	count = 0
	indicesPrinted=[]
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

def DisplayBoardState(state, current):
	#print '\nBank = ', state.bank.cash
	clear()
	#print '####################################################################'
	#print " 			",current.name#, "'s turn!"					
	#print '#########################################'
	PrintCoins(state.bank.cash,10)
	for each in state.players:
		print''
		if each == current:
			print '***', current.name,'***'
		else:
			print '   ', each.name
		print '------------'
		for card in each.hand:
			if card.dead:
				print 'X ', card.name 
			elif each == current:
				print '? ', card.name
			else:
				print '?'

		PrintCoins(each.cash,5)
	print ''
	return

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

def GameOverScreen(state,winner):
	DisplayBoardState(state,winner)
	print 'Game Over'
	print winner.name, " WINS !!!"
	print 
	response = DisplayOptions('Play Again?',['Yes','No'],False)
	if response =='Yes':
		#Play()
		exit()
	else:
		clear()
		exit()
	return

