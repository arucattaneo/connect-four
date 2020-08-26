import random

def createBoard(number, table, character):
	for i in range (number):
		row = []
		for j in range (number):			
			row.append(character)
		table.append(row)

def printBoard(table):
	for i in range (len(table)):
		for j in range (len(table)):
			print(f" {table[i][j]} ", end=" ")
		print(i+1)
	#Last row
	for i in range (len(table)):
		if i < 9:
			print(f" {i+1}  ", end="")
		else:
			print(f"{i+1}  ", end="")
	print()

def getReverse(reverseProbability):
	num = random.randint(1,10)
	if(num <= reverseProbability):
		return 1
	return 0

def getHope(hopeProbability):
	num = random.randint(1,10)
	if(num <= hopeProbability):
		return 1
	return 0

def getTokens(tokens, hopeProbability, reverseProbability):
	tokens[0] += 1
	if tokens[1] < 1:
		tokens[1] += getHope(hopeProbability)
	tokens[2] += getReverse(reverseProbability)
	

def validateNumber(table):
	valid = False
	num = input(f"Insert a number between 1 and {len(table)}: ")
	while (not valid):
		if(not num.isnumeric()):
			print(f"{num} is not a number")
			num = input(f"{num} is not a number\nRetry: ")

		elif(int(num) < 1 or int(num) > len(table)):
			num = input("Invalid number\nRetry: ")

		else:
			valid = True

	return int(num)

def validateColumn(table, character):
	valid = False
	while(not valid):
		print("Column: ")
		column = validateNumber(table) - 1
		if (table[0][column] != character):
			print("That column is full\nRetry: ")
			column = validateNumber(table) - 1
		else:
			valid = True
	return column 

def playReverse(table, character, column, token1, token2):
	played = False
	while not played:
		for i in range (len(table)):
			if not played:
				if(table[i][column] == token2):
					table[i][column] = token1
					played = True

		if(not played):
			print("There are no tokens to revert in that column\nRetry: ")
			column = validateColumn(table, character)

def playToken(table, character, column, token1, token2, option):
	played = False
	row = len(table) - 1
	while not played:
		if(option == '1' or option == '2'):
			if(table[row][column] == character):			
				table[row][column] = token1			
				played = True
			else:
				row -= 1
		elif(option == '3'):
			playReverse(table, character, column, token1, token2)
			played = True	
				

def chooseToken(tokens):
	valid = False
	print("Tokens available:")
	print(f"1) Standard {tokens[0]}\n2) Hope: {tokens[1]}\n3) Reverse: {tokens[2]}")
	option = input("Which one do you want to choose? [1, 2, 3]: ")
	while option != '1' and option != '2' and option != '3':
		option = input("Invalid option\nWhich one do you want to choose? [1, 2, 3]: ")
	while not valid:
		if(tokens[int(option)-1] == 0):
			print("You do not have any more tokens of that type")
			option = input("Retry: ")
			while option != '1' and option != '2' and option != '3':
				option = input("Invalid option\nWhich one do you want to choose? [1, 2, 3]: ")
		else:
			valid = True
	return option


def play(table, character, token1, token2, winningAmount, option):
	column = validateColumn(table, character)
	playToken(table, character, column, token1, token2, option)
	printBoard(table)
		

def turn(table, character, token1, token2, winningAmount, tokens, hopeProbability, reverseProbability):
	getTokens(tokens, hopeProbability, reverseProbability)
	option = chooseToken(tokens)
	if option == '1':
		play(table, character, token1, token2, winningAmount, option)
		tokens[0] -= 1
	elif option == '2':
		play(table, character, token1, token2, winningAmount, option)
		tokens[1] -= 1

		option = chooseToken(tokens)
		if(option == '1'):
			play(table, character, token1, token2, winningAmount, option)
			tokens[0] -= 1
		elif(option == '2'):
			print("Sorry, you can't play two reverse tokens in a row")
		elif(option == '3'):
			play(table, character, token1, token2, winningAmount, option)
			tokens[2] -= 1
	else:
		play(table, character, token1, token2, winningAmount, option)
		tokens[2] -= 1

def checkHorizontals(table, winningAmount, token1, token2):
	for row in table:
		player1 = 0
		player2 = 0

		for token in row:
			if(token == token1):
				player1 += 1				
				player2 = 0
				if(player1 == winningAmount):
					print(f"Player 1 ({token1}) has won!")
					return 0

			elif(token == token2):
				player2 += 1				
				player1 = 0
				if(player2 == winningAmount):
					print(f"Player 2 ({token2}) has won!")
					return 1
	return -1

def checkVerticals(table, winningAmount, token1, token2):
	for column in range (len(table)):
		player1 = 0
		player2 = 0		

		for row in range (len(table)):
			if(table[row][column] == token1):
				player1 += 1				
				player2 = 0
				if(player1 == winningAmount):
					print(f"Player 1 ({token1}) has won!")
					return 0

			elif(table[row][column] == token2):
				player2 += 1				
				player1 = 0
				if(player2 == winningAmount):
					print(f"Player 2 ({token2}) has won!")
					return 1
	return -1

def checkDiagonals(table, winningAmount, token1, token2):
	'''
	  *
	 *
	*
	'''
	# First half of the board
	for i in range(3, len(table)):
		player1 = 0
		player2 = 0

		for j in range (0, i+1):
			if(table[i][j] == token1):
				player1 += 1
				player2 = 0				
				if(player1 == winningAmount):
					print(f"Player 1 ({token1}) has won!")
					return 0

			elif(table[i][j] == token2):
				player2 += 1
				player1 = 0
				if(player2 == winningAmount):
					print(f"Player 2 ({token2}) has won!")
					return 1
			i -= 1

	# Second half of the board
	for i in range(1, len(table)-3):
		player1 = 0
		player2 = 0

		for j in range (len(table)-1, i-1, -1):
			if(table[i][j] == token1):
				player1 += 1
				player2 = 0
				if(player1 == winningAmount):
					print(f"Player 1 ({token1}) has won!")
					return 0

			elif(table[i][j] == token2):
				player2 += 1
				player1 = 0
				if(player2 == winningAmount):
					print(f"Player 2 ({token2}) has won!")
					return 1
			i += 1

	'''
	*
	 *
	  *
	'''
	# First half of the board
	counter1 = 3
	for i in range(3, len(table)):
		player1 = 0
		player2 = 0

		for j in range (len(table)-1, counter1, -1):
			if(table[i][j] == token1):
				player1 += 1
				player2 = 0				
				if(player1 == winningAmount):
					print(f"Player 1 ({token1}) has won!")
					return 0

			elif(table[i][j] == token2):
				player2 += 1
				player1 = 0
				if(player2 == winningAmount):
					print(f"Player 2 ({token2}) has won!")
					return 1
			i -= 1
		counter1 -= 1

	# Second half of the board
	counter2 = len(table) - 1
	for i in range(1, len(table)-3):
		player1 = 0
		player2 = 0		

		for j in range (0, counter2):
			if(table[i][j] == token1):
				player1 += 1
				player2 = 0
				if(player1 == winningAmount):
					print(f"Player 1 ({token1}) has won!")
					return 0

			elif(table[i][j] == token2):
				player2 += 1
				player1 = 0
				if(player2 == winningAmount):
					print(f"Player 2 ({token2}) has won!")
					return 1
			i += 1
		counter2 -= 1
	return -1

def checkWin(table, token1, token2, winningAmount):	
	horiz = checkHorizontals(table, winningAmount, token1, token2)
	vert = checkVerticals(table, winningAmount, token1, token2)
	diag = checkDiagonals(table, winningAmount, token1, token2)
	if(horiz != -1):
		return horiz
	
	elif(vert != -1):
		return vert

	elif(diag != -1):
		return diag

	else:
		return -1

def gameRound(table, character, players, token1, token2, winningAmount, tokensPlayer1, tokensPlayer2, hopeProbability, reverseProbability):
	end = -1
	while end == -1:
		print(f"{players[0]}'s turn ({token1}): ")
		turn(table, character, token1, token2, winningAmount, tokensPlayer1, hopeProbability, reverseProbability)
		end = checkWin(table, token1, token2, winningAmount)
		if end == -1:
			print(f"{players[1]}'s turn ({token2}): ")
			turn(table, character, token2, token1, winningAmount, tokensPlayer2, hopeProbability, reverseProbability)
			end = checkWin(table, token1, token2, winningAmount)
	return end

def startGame(size, table, character, players, token1, token2, winningAmount, tokensPlayer1, tokensPlayer2, hopeProbability, reverseProbability, score):
	createBoard(size, table, character)
	printBoard(table)
	winner = gameRound(table, character, players, token1, token2, winningAmount, tokensPlayer1, tokensPlayer2, hopeProbability, reverseProbability)
	print(f"Congratulations {players[winner]}! You won this round")
	score[winner] += 1

def validateProbability():
	valid = False
	num = input("Insert a number from 1-10 to adjust the probability: ")
	while (not valid):
		if not num.isnumeric():
			num = input(f"{num} is not a number\nRetry: ")
		else:
			if int(num) < 0 or int(num) > 10:
				num = input("The number is not in the specified range\nRetry: ")
			else:
				valid = True
	return int(num)

def adjustSize():
	SizeOption = input("Board SizeOption:\n1) 8x8\n2) 15x15\n3) 20x20\n[1, 2, 3]: ")
	while SizeOption != '1' and SizeOption != '2' and SizeOption != '3':
		SizeOption = input("Invalid Option\nRetry: ")
	if SizeOption == '1':
		size = 8
	elif SizeOption == '2':
		size = 15
	else:
		size = 20
	return size

def main():
	character = "~"
	token1 = "x"
	token2 = "o"	

	winningAmount = 4
	finished = False
	score = [0,0]
	hopeProbability = 4
	reverseProbability = 1
	size = 8

	print("----- CONNECT FOUR -----\n\n")

	player1 = input("Player 1 insert your name: ").capitalize()
	player2 = input("Player 2 insert your name: ").capitalize()
	players = (player1, player2)

	while (not finished):
		table = []
		#index 0: standard, index 1: hope, index 2: reverse
		tokensPlayer1 = [0,0,0]
		tokensPlayer2 = [0,0,0]

		print("1) Start Game\n2) Adjust parameters\n3) Show score\n4) Exit")
		option = input("Choose an option [1, 2, 3, 4]: ")

		while(option != '1' and option != '2' and option != '3' and option != '4'):
			option = input("Invalid Option\nRetry: ")

		if option == '1':
			startGame(size, table, character, players, token1, token2, winningAmount, tokensPlayer1, tokensPlayer2, hopeProbability, reverseProbability, score)
		
		elif option == '2':
			size = adjustSize()
			print("Token: Hope")
			hopeProbability = validateProbability()
			print("Token: Reverse")
			reverseProbability = validateProbability()			

		elif option == '3':
			print(f"Score\n{players[0]}({token1}): {score[0]}, {players[1]}({token2}): {score[1]}")

		else:
			finished = True

main()