# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time

class Game:
	HUMAN = 2
	AI = 3

	def __init__(self, recommend = True, n, b, b_pos = [], s, t):
		self.recommend = recommend
		self.n = n # NOTE: size of the board
		self.b = b # BUG: Number of blocks
		self.b_pos = b_pos # position of the blocks
		self.s = s # winning line-up size
		self.d1 = d1 # max depth1
		self.d2 = d2 # max depth2
		self.t = t # max allowed time
		self.a = a # boolean for algorithm: Minimax(false) or Alphabeta(true)

		self.initialize_game()

	def initialize_game(self):

		for i in range(self.n):
            		row = []
            		for j in range(self.n):
                		row.append('.')
            		self.current_state.append(row)
		
		# For making the blocs
		for blocs in self.b_pos:
			#self.current_state[][] = '*'

		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		ch = 'A'
        	print()
       		print("    ", end="")
        	for y in range(0,self.n): 
            		print(chr(ord(ch) + y) + " ", end="")
        	print()
        
        	for y in range(0,self.n):
           		print(str(y) + " | ", end="")
            		for x in range(0, self.n):
                		print(F'{self.current_state[x][y]}' + " ", end="")
            		print()
        	print()

	def is_valid(self, px, py):
		 if px < 0 or px > (self.n-1) or py < 0 or py > (self.n-1):
		 	return False
		 elif self.current_state[px][py] != '.':
		 	return False
		 else:
		 	return True

	def is_end(self):
		# Making the Win condition for X & O from the winning size
		WinO = 'O' * self.s # Checking if it's is (n) number of Os
	    	WinX = 'X' * self.s # Checking if (n) number of Xs
	    
		# Vertical win
		# Loops through the board columns and saves the values in a list and then checks if the saved value WinO or WinX is part of that list and returns X or O
	    	for i in range(0, self.s):
			colWin = [col[i] for col in self.current_state]
		    	columnWin = "".join(str(j) for j in colWin)
		     
		    	if (WinO in columnWin):
		        	return 'O'
		    	if (WinX in columnWin):
		        	return 'X'
		# Horizontal win
		for i in range(0, self.s):
			rowWin = "".join(str(j) for j in self.current_state[i])
		    	if (WinO in rowWin):
		 		return 'O'
		 	elif (WinX in rowWin):
		 		return 'X'
		
		# Diagonals win
		 #if (self.current_state[0][0] != '.' and
		 #	self.current_state[0][0] == self.current_state[1][1] and
		 	#self.current_state[0][0] == self.current_state[2][2]):
		 	#return self.current_state[0][0]
		
		# # Second diagonal win
		# if (self.current_state[0][2] != '.' and
		# 	self.current_state[0][2] == self.current_state[1][1] and
		# 	self.current_state[0][2] == self.current_state[2][0]):
		# 	return self.current_state[0][2]
		
		# Is whole board full? Stays the same
		 for i in range(0, self.n):
		 	for j in range(0, self.n):
		 		# There's an empty field, we continue the game
		 		if (self.current_state[i][j] == '.'):
		 			return None
		# It's a tie!
		return '.'

	
	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
		 		print('The winner is X!')
		 	elif self.result == 'O':
		 		print('The winner is O!')
		 	elif self.result == '.':
		 		print("It's a tie!")
		 	self.initialize_game()
		 return self.result

	def input_move(self):
		# while True:
		# 	print(F'Player {self.player_turn}, enter your move:')
		# 	px = int(input('enter the x coordinate: '))
		# 	py = int(input('enter the y coordinate: '))
		# 	if self.is_valid(px, py):
		# 		return (px,py)
		# 	else:
		# 		print('The move is not valid! Try again.')

	def switch_player(self):
		# if self.player_turn == 'X':
		# 	self.player_turn = 'O'
		# elif self.player_turn == 'O':
		# 	self.player_turn = 'X'
		# return self.player_turn

	def minimax(self, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max:
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self,algo=None,player_x=None,player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					# if self.recommend:
					# 	print(F'Evaluation time: {round(end - start, 7)}s')
					# 	print(F'Recommended move: x = {x}, y = {y}')
					# (x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	board_size = int(input("Enter size of the board: "))
	blocks_num = int(input("Enter number of blocks : "))
	blocks_pos= []
	print('Enter position of the blocks followed by ENTER key:')
	print('Please follow the syntax: \'row number,column\'')
	# getting block positions
	for i in range(0, blocks_num):
		e = input()
		blocks_pos.append(e) # adding the element
	print(blocks_pos)
	lineup_size = int(input('Enter the winning line-up size:'))

	max_time = float(input('Enter the maximum allowed time for the program: '))

	print('Player \'X\' mode: ')
	player_x = input('Press 2 for Human, 3 for AI : ')
	depth1 = None
	if player_x == '3':
		depth1 = int(input('Enter the maximum depth of the adversarial search for player X: '))
	print('Player \'O\' mode: ')
	player_o = input('Press 2 for Human, 3 for AI : ')
	depth2 = None
	if player_o == '3':
		depth2 = int(input('Enter the maximum depth of the adversarial search for player O: '))

	algo = input('Please specify the algorithm, 0 for Minimax, 1 for Alphabeta')
		if algo == '0':
			a = False
		else:
			a = True


	g = Game(board_size, blocks_num, blocks_pos, lineup_size, max_time)
	g.play(algo, player_x, player_o, depth1, depth2)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

	# Game Trace Output File
	gameTraceName = "gameTrace-" + str(self.n) + str(self.b) + str(self.s) + str(self.t)
	f = open(gameTraceName, "w+")
	f.write("n= %d\t" %self.n, "b= %d\t" %self.b, "s= %d\t" %self.s, "t= %d\t" %self.t)
	f.write("blocs= [ %d" %self.b_pos, "]", "\n")

	f.write("Player 1: d= %d\t" %self.d1, "a= %s", "e1( %s", ")" ) # Add the true value and the heuristic e1
	f.write("Player 2: d= %d\t" %self.d2, "a= %s", "e2( %s", ")" ) # Add the true value and the heuristic e2
	f.write("\n")

if __name__ == "__main__":
	main()
