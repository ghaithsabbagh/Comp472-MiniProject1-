# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import math
import numpy as np
import random

class Game:
	HUMAN = 2

	def __init__(self, n, b, b_pos, s, t, d1, d2, a):
		self.n = n # size of the board
		self.b = b # Number of blocks
		self.bloc_pos = b_pos # position of the blocks
		self.s = s # winning line-up size
		self.depth1 = d1 # max depth1
		self.depth2 = d2 # max depth2
		self.t = t # max allowed time
		self.a = a # boolean for algorithm: Minimax(false) or Alphabeta(true)

		self.initialize_game()

	def initialize_game(self):

		# Making the nxn board
		self.current_state = [ ['.'] * self.n for j in range(self.n) ]
		# rows = self.n
		# cols = self.n
		# self.current_state = [['.']*cols]*rows

		# For making the blocs, if given it will generate the one chosen if not then the blocs will be places in random places using randint
		if self.bloc_pos:
			for i in range(len(self.bloc_pos)):
				chars = list(self.bloc_pos[i])
				b1 = int(chars[0])
				b2 = ord(chars[1])-65
				if self.is_valid(b1, b2):
					self.current_state[b1][b2] = '*'
				else:
					print("invalid!!")
					break
		else:
			for i in range(0, self.b):
				b1 = random.randint(0, self.n - 1)
				b2 = random.randint(0, self.n - 1)

		# Player X always plays first
		self.player_turn = 'O'

	def draw_board(self):
		ch = 'A'
		print()
		print("    ", end="")
		for y in range(0, self.n):
			print(chr(ord(ch) + y) + " ", end="")
		print()

		for x in range(0, self.n):
			print(str(x) + " | ", end="")
			for y in range(0, self.n):
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
		# Making the Win conditions for X & O from the winning size
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


		# Is whole board full? (Stays the same)
		for i in range(0, self.n):# There's an empty field, we continue the game
			for j in range(0, self.n):
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
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = input('enter the y coordinate in CAPS: ')
			py_number = ord(py) - 65
			if self.is_valid(px, py_number):
				return (px,py_number)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def countNumEmpty(self, config):
		counter = 0
		for i in range(0, self.n - 1):
			for j in range(0, self.n - 1):
				if config[i][j] == '.':
					counter += 1
		return counter

	def heuristic_func(self, board, h):
		no = 0
		nx = 0
		empty = 0
		eval2 = 0
		if h == 1:		# Default heuristic
			ne = self.countNumEmpty(board)
			for i in range(0, self.n):
				for j in range(0, self.n):
					if board[i][j] == 'O':
						no += 1		# counts nuber of 'O'
					elif board[i][j] == 'X':
						nx += 1	# counts the number of 'X'
			if no == nx and no < self.s:
				eval = int((no * (ne+1))/(self.n - 1))
			eval = int((no - nx)*(ne + 1)/(self.s - 1))
			return eval
		else:			# Smart hueristic counts the number of X or O for corresponding player and considers empty spots
			for i in range (0, self.n):
				for j in range (0, self.n):
					if board[i][j] == '.':
						empty += 1
					elif board[i][j] == 'O':
						no =+ 1
					elif board[i][j] == 'X':
						nx += 1
				if (self.s - no) >= empty:
					eval2 += empty
				else:
					eval2 -= empty
				empty = 0
				no = 0
				nx = 0
			board_copy = np.copy(board)
			board_t = board_copy.T		# get the transpose of the board to iterate through columns
			for i in range (0, self.n):
				for j in range (0, self.n):
					if board_t[i][j] == '.':
						empty += 1
					elif board_t[i][j] == 'O':
						no += 1
					elif board_t[i][j] == 'X':
						nx += 1
				if (self.s - no) >= empty:
					eval2 += empty
				else:
					eval2 -= empty
				empty = 0
				no = 0
				nx = 0
			return eval2

	def minimax(self, isMaximizer, depth, heuristic, board):
		maxEval = -10000
		minEval = 10000
		result = self.is_end()
		if result == 'X':
			return (-100, x, y)
		elif result == 'O':	# player 'O' wins
			return (100, x, y)
		elif result == '.':	# The game is a tie
			return (0, x, y)
		else:
			if depth == 0:
				return self.heuristic_func(board, heuristic)
		if isMaximizer:
			for i in range(0, self.n - 1):
				for j in range(0, self.n -1):
						if board[i][j] == '.':
							board[i][j] = 'O'
							eval = self.minimax(False, depth-1, heuristic, board)
							board[i][j] = '.'
							if eval > maxEval:
								maxEval = eval
								x = i
								y = j
			if depth == 3:
				return (maxEval, x, y)
			return maxEval

		else:
			for i in range(0, self.n - 1):
				for j in range(0, self.n -1):
					if board[i][j] == '.':
							board[i][j] = 'X'
							eval = self.minimax(True, depth -1, heuristic, board)
							board[i][j] = '.'
							if eval < minEval:
								minEval = eval
								x = i
								y = j
			if depth == 3:
				return (minEval, x, y)
			return minEval


	def alphabeta(self, isMaximizer, depth, heuristic, board, alpha, beta):
		# We're initially setting it to 2 or -2 as worse than the worst case:
		result = self.is_end()
		if result == 'X':
			return (-100, x, y)
		elif result == 'O':
			return (100, x, y)
		elif result == '.':
			return (0, x, y)
		else:
			if depth == 0:
				return self.heuristic_func(board, heuristic)
		if isMaximizer:
			numEmptySpots = self.countNumEmpty(board) #find the number of empty blocks
			for k in range (numEmptySpots):	#For each child of the node
				boardCopy = np.copy(board)	# make copies/number of empty blocks
				for i in range (0, self.n - 1):
					for j in range (0, self.n -1):
						if boardCopy[i][j] == '.':
							boardCopy[i][j] = 'O'
							if i == 0 and j == 0:
								maxEval = -1000
							eval = self.alphabeta(False, depth-1, heuristic, boardCopy, alpha, beta)
							if eval > maxEval:
								maxEval = eval
								x = i
								y = j
							alpha = max(alpha, eval)
							if beta <= alpha:
								break

				return maxEval
		else:
			numEmptySpots = self.countNumEmpty(board) #find the number of empty blocks
			for k in range (numEmptySpots):
				boardCopy = np.copy(board)	# make copies/number of empty blocks
				for i in range (0, self.n - 1):
					for j in range (0, self.n -1):
						if boardCopy[i][j] == '.':
							boardCopy[i][j] = 'X'
							if i == 0 and j == 0:
								minEval = 1000
							eval = self.alphabeta(True, depth -1, heuristic, boardCopy, alpha, beta)
							if eval < minEval:
								minEval = eval
								x = i
								y = j
							beta = min(beta, eval)
				return minEval

	def play(self,player_x,player_o):

		while True:
			self.draw_board()
			if self.check_end():
				return
			# start = time.time()
			if player_o.get('mode') == 'HUMAN' and self.player_turn == 'O':
				(x,y) = self.input_move()
			elif player_x.get('mode') == 'HUMAN' and self.player_turn == 'X':
				(x,y) = self.input_move()
			elif player_o.get('mode') == 'AI' and self.player_turn == 'O':
				if self.a == False:
					(_, x, y) = self.minimax(True, player_o.get('depth'), player_o.get('heuristic'), self.current_state)
				else:
					(_, x, y) = self.alphabeta(True, player_o.get('depth'), player_o.get('heuristic'), self.current_state, alpha= -math.inf, beta= math.inf)
			elif player_x.get('mode') == 'AI' and self.player_turn == 'X':
				if self.a == False:
					(_, x, y) = self.minimax(False, player_x.get('depth'), player_x.get('heuristic'), self.current_state)
				else:
					(_, x, y) = self.alphabeta(False, player_x.get('depth'), player_x.get('heuristic'), self.current_state, alpha= -math.inf, beta= math.inf)


			# end = time.time()

			self.current_state[x][y] = self.player_turn # fills the board with 'X' or 'O'
			self.switch_player()

def main():
	board_size = int(input("Enter size of the board: "))
	blocks_num = int(input("Enter number of blocks : "))
	blocks_pos= []
	print('Enter position of the blocks followed by ENTER key:')
	print('Please follow the syntax: \'row number,column in CAPS\'')
	# getting block positions
	for i in range(0, blocks_num):
		e = input()
		blocks_pos.append(e) # adding the element
	print(blocks_pos)
	lineup_size = int(input('Enter the winning line-up size:'))
	max_time = float(input('Enter the maximum allowed time for the program: '))

	print('Player \'X\' mode: ')
	mode_x = int(input('Press 2 for Human, 3 for AI : '))
	if mode_x == 3:
		depth1 = int(input('Enter the maximum depth of the adversarial search for player X: '))
		h1 = int(input('Press 1 for the default heuristic, 2 for smart heuristic: '))

	print('Player \'O\' mode: ')
	mode_o = int(input('Press 2 for Human, 3 for AI : '))
	if mode_o == 3:
		depth2 = int(input('Enter the maximum depth of the adversarial search for player O: '))
		h2 = int(input('Press 1 for the default heuristic, 2 for smart heuristic: '))

	algo = input('Please specify the algorithm, 0 for Minimax, 1 for Alphabeta')
	if algo == '0':
		a = False
	else:
		a = True
	# Setting up variables for player_o and player_x if the mode is 'AI'
	if mode_x == 3:
		player_x = {'mode': 'AI', 'algo': a, 'depth': depth1, 'heuristic': h1}
	else:
		player_x = {'mode': 'HUMAN'}
		depth1 = None
	if mode_o == 3:
		player_o = {'mode': 'AI', 'algo': a, 'depth': depth2, 'heuristic': h2 }
	else:
		player_o = {'mode': 'HUMAN'}
		depth2 = None

	g = Game(board_size, blocks_num, blocks_pos, lineup_size, max_time, depth1, depth2, a)
	g.play(player_x, player_o)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()
