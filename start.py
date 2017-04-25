import random
import Cards 

# main update loop - not sure how its gonna work yet
def Update():
	return

# Called at start, make deck and stuff
def InitializeGame():
	
	CardTypes = ["Assassin","Duke","Captain", "Ambassador", "Contessa" ]
	deck = []
	for type in CardTypes:
		for num in range (1,4):
			deck.append(Cards.Card(type))
	
	Cards.ShuffleDeck(deck)	
	Cards.PrintDeck(deck)
	
	return deck





#called at run-time
def main():
	deck = InitializeGame()
	while(True):
		Cards.PromptPlayer(deck)	


if __name__=="__main__":
	main()