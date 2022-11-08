#coding:utf-8

#######################################
## --- C O V I - S C R A B B L E --- ##
## Copyright (c) Jérôme Lehuen 2022  ##
#######################################

#########################################################################
##                                                                     ##
##   This file is part of COVI-SCRABBLE version 1.1                    ##
##                                                                     ##
##   COVI-SCRABBLE is free software: you can redistribute it and/or    ##
##   modify it under the terms of the GNU General Public License as    ##
##   published by the Free Software Foundation, either version 3 of    ##
##   the License, or (at your option) any later version.               ##
##                                                                     ##
##   COVI-SCRABBLE is distributed in the hope that it will be useful   ##
##   but WITHOUT ANY WARRANTY - without even the implied warranty of   ##
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.              ##
##                                                                     ##
##   See the GNU General Public License for more details. You should   ##
##   have a copy of the GNU GPLv3 along with COVI-SCRABBLE.            ##
##   If not, see https://www.gnu.org/licenses/                         ##
##                                                                     ##
##   The game named SCRABBLE is trademarked by Mattel Inc. and Hasbro  ##
##                                                                     ##
#########################################################################

import threading
from tkinter import *
from utils import *
from constants import *
from letter import Letter
from scra_client import Client
from winscore import Winscore
from calculator import calculer_score
from dico.dictionary import Dictionary

class Scrabble(Tk):

	canvas = None
	board = None    # Matrix [0..14][0..14] of letters
	stand = None    # List of letters
	bag = None      # Character deck
	mot = None      # Letters of the last word
	dico = None     # Lexicographic dictionary
	login = None    # Player Login
	passwd = None   # Player Password
	locked = True   # Player lock

	##########################
	## Scrabble constructor ##
	##########################

	def __init__(self, VERSION, LANG, addr, port, userdata, serverflag):
		super().__init__()

		self.LANG = LANG
		self.login = userdata[0]
		self.title('C O V I S C R A B B L E  %d.%d  –  %s' % (VERSION[0], VERSION[1], self.login))
		self.resizable(False, False)

		# Create the board
		self.build_board()

		# Create the buttons
		MARGIN = 10
		if serverflag: Button(self, text='  Start Game  ', command=self.restart).pack(side=LEFT, padx=MARGIN, pady=MARGIN)
		Button(self, text='  Exit Game  ', command=quit).pack(side=RIGHT, padx=MARGIN, pady=MARGIN)
		self.btn_valider = Button(self, text='  Validate  ', state=DISABLED, command=self.valider)
		self.btn_valider.pack(side=BOTTOM, padx=MARGIN, pady=MARGIN)

		center(self)

		# Create the score window
		self.winscore = Winscore(self)
		self.update_winscore_position()
		self.bind('<Configure>', self.dragging)

		# Initialize the board and the stand models
		self.board = [[None] * 15 for _ in range(15)]
		self.stand = []
		self.mot = []

		# Load the dictionary
		name = 'dico_%s' % LANG
		self.dico = Dictionary(name)

		# Launch the client
		self.client = Client(VERSION, addr, port, userdata)
		client_thread = threading.Thread(target=self.client.run)
		client_thread.daemon = True
		client_thread.start()

	def build_board(self):
		self.canvas = Canvas(self, width=BOARD_WIDTH-4, height=TOTAL_HEIGHT-4)
		# Draw the board
		for li in range(15):
			for co in range(15):
				x = co * WIDTH
				y = li * HEIGHT
				if   BOARD_VAL1[li][co] == 2: color = COLOR_BLUE1
				elif BOARD_VAL1[li][co] == 3: color = COLOR_BLUE2
				elif BOARD_VAL2[li][co] == 2: color = COLOR_RED1
				elif BOARD_VAL2[li][co] == 3: color = COLOR_RED2
				else: color = COLOR_NONE
				self.canvas.create_rectangle(x, y, x+WIDTH, y+HEIGHT, fill=color, width=3, outline='white')
		# Draw the stand
		self.canvas.create_rectangle(0, BOARD_HEIGHT, BOARD_WIDTH, TOTAL_HEIGHT, fill='green', width=3, outline='white')
		self.canvas.create_line(0, BOARD_HEIGHT + HEIGHT, BOARD_WIDTH, BOARD_HEIGHT + HEIGHT, fill=COLOR_LINE)
		self.canvas.create_line(0, BOARD_HEIGHT + 2*HEIGHT, BOARD_WIDTH, BOARD_HEIGHT + 2*HEIGHT, fill=COLOR_LINE)
		self.canvas.pack(side=TOP)

	#####################
	## Private methods ##
	#####################

	def dragging(self, event):
		# https://stackoverflow.com/questions/45183914/tkinter-detecting-a-window-drag-event
		if event.widget is self: self.update_winscore_position()

	def update_winscore_position(self):
		self.update() # Before getting winfo values
		x = self.winfo_x() + self.winfo_width() + 10
		y = self.winfo_y()
		self.winscore.geometry('+%d+%d' % (x,y))
		self.winscore.lift() # In the foreground

	def restart(self):
		self.client.restart()

	############################################
	## Model methods (not a real MVC pattern) ##
	############################################

	def free(self, li, co):
	 	return self.board[li][co] is None

	def put(self, letter, li, co):
		self.board[li][co] = letter # Add to the board
		self.stand.remove(letter) # Remove from the stand
		self.mot.append(letter) # To count the points
		self.client.put(letter.key, li, co, letter.jocker)

	def get(self, letter):
		self.board[letter.li][letter.co] = None # Remove from the board
		self.stand.append(letter) # Add to the stand
		self.mot.remove(letter) # To count the points
		self.client.get(letter.li, letter.co)

	def calculer_score(self):
		return calculer_score(self.board, self.mot, self.dico)

	def valider(self):
		self.btn_valider.configure(state=DISABLED)
		mot,score = self.calculer_score()
		if score:
			self.lock_all_letters()
			nblettres = 7-len(self.stand) # Number of letters to pick
			self.client.valider(mot, score, nblettres)
		else:
			self.btn_valider.configure(state=NORMAL)

	def clear_canvas(self):
		# Delete letters from the stand
		for letter in self.stand: letter.delete()
		# Delete letters from the board
		for li in range(15):
			for co in range(15):
				letter = self.board[li][co]
				if letter: letter.delete()

	def lock_all_letters(self):
		for li in range(15):
			for co in range(15):
				letter = self.board[li][co]
				if letter: letter.lock()

	#####################################
	## Methods invoked from the server ##
	#####################################

	def pool(self):
		# To consult the client every 500 ms
		self.client.process_messages(self)
		self.after(500, self.pool)

	def async_put(self, key, li, co, jocker):
		if jocker:
			letter = Letter(' ', li, co, self).setKey(key)
		else:
			letter = Letter(key, li, co, self)
		self.board[li][co] = letter
		letter.lock()

	def async_get(self, li, co):
		letter = self.board[li][co]
		self.board[li][co] = None
		letter.delete()

	def async_score(self, login, mot, score):
		#print('Score of %s for %s = %d' % (login, mot, score))
		self.winscore.newscore(login, mot, score)

	def async_addstand(self, liste):
		# Reposition the old letters
		for i,letter in enumerate(self.stand):
			letter.setLC(16, i+4)
		# Position the new letters
		for i,key in enumerate(liste):
			self.stand.append(Letter(key, 17, i+4, self))

	def async_player(self, login):
		if login == self.login:
			self.btn_valider.configure(state=NORMAL)
			self.locked = False
			self.mot = []
		else:
			self.btn_valider.configure(state=DISABLED)
			self.locked = True

	def async_restart(self):
		self.clear_canvas()
		self.winscore.reset()
		self.board = [[None] * 15 for _ in range(15)]
		self.stand = []
		self.mot = []

	def async_gameover(self, login):
		print('GAME OVER')
		# Redistribute stand points
		somme = sum(lettre.value for lettre in self.stand)
		self.client.redonner(somme, login)

	def async_transfer(self, expediteur, destinataire, somme):
		self.winscore.newscore(expediteur, '', -somme)
		self.winscore.newscore(destinataire, '', somme)
		# Game over popup window
		title = 'The player %s put down the last letter' % destinataire
		Splashwin(self, title, 'data/gameover.png', False)
