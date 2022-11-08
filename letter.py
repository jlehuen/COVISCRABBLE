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

from tkinter import *
from tkinter.font import Font
from tkinter.simpledialog import askstring
from string import ascii_uppercase

from constants import *
from polygon import RoundedRectangle

class Letter():

	x0 = None
	y0 = None
	key = None       # Character to display
	val = None       # Value of the letter
	canvas = None    # The graphic canvas
	scrabble = None  # The main class
	locked = False   # Lock of the letter
	jocker = False   # Flag if jocker

	########################
	## Letter constructor ##
	########################

	def __init__(self, key, li, co, scrabble):
		self.li = li
		self.co = co
		self.x0 = co * WIDTH
		self.y0 = li * HEIGHT
		self.key = key
		self.val = eval('BAG_%s[key][0]' % scrabble.LANG)
		self.jocker = key == ' '
		self.scrabble = scrabble
		self.canvas = scrabble.canvas
		
		x,y = self.x0,self.y0
		# The fonts must be defined after the Tkinter root
		FONT1 = Font(family='Verdana', size=int(WIDTH / 1.8)) # Font of the letter
		FONT2 = Font(family='Verdana', size=int(WIDTH / 4)) # Font of the value
		# Draw the 3 items of the tile
		self.item1 = self.create_roundedRectangle(x, y)
		self.item2 = self.canvas.create_text(x+WIDTH/2, y+HEIGHT/2, text=key, font=FONT1, anchor=CENTER)
		self.item3 = self.canvas.create_text(x+WIDTH/10*9, y+HEIGHT/10*8, text=self.val, font=FONT2, anchor=E)
		# Link the mouse actions for each item
		self.canvas.tag_bind(self.item1.get_polygon(), '<Button-1>', self.mouse_clic)
		self.canvas.tag_bind(self.item1.get_polygon(), '<Button1-Motion>', self.mouse_move)
		self.canvas.tag_bind(self.item1.get_polygon(), '<ButtonRelease-1>', self.mouse_release)
		self.canvas.tag_bind(self.item2, '<Button-1>', self.mouse_clic)
		self.canvas.tag_bind(self.item3, '<Button-1>', self.mouse_clic)
		self.canvas.tag_bind(self.item2, '<Button1-Motion>', self.mouse_move)
		self.canvas.tag_bind(self.item3, '<Button1-Motion>', self.mouse_move)
		self.canvas.tag_bind(self.item2, '<ButtonRelease-1>', self.mouse_release)
		self.canvas.tag_bind(self.item3, '<ButtonRelease-1>', self.mouse_release)


	def create_roundedRectangle(self, x, y):
		COLOR1 = 'blanchedalmond' # 255, 235, 205
		COLOR2 = '#%02X%02X%02X' % (245, 225, 195)
		return RoundedRectangle(self.canvas, x, y, WIDTH, HEIGHT, 3, width=0, fill=COLOR1, outline=COLOR2)

	############################
	## Mouse listener methods ##
	############################

	def mouse_clic(self, event):
		if not self.locked:
			# Bring back the tile to the front
			self.canvas.tag_raise(self.item1.get_polygon())
			self.canvas.tag_raise(self.item2)
			self.canvas.tag_raise(self.item3)
			# Memorize the initial point
			self.xold = event.x
			self.yold = event.y
			self.grab()


	def mouse_move(self, event):
		if not self.locked:
			# Calculate the offsets
			dx = event.x - self.xold
			dy = event.y - self.yold
			if self.x0 + dx < 0: dx = 0
			if self.y0 + dy < 0: dy = 0
			if self.x0 + dx + WIDTH > BOARD_WIDTH: dx = 0
			if self.y0 + dy + HEIGHT > TOTAL_HEIGHT: dy = 0
			# Move the tile
			self.move(dx, dy)
			# Memorize the last point
			self.xold = event.x
			self.yold = event.y

	def mouse_release(self, event):
		if not self.locked:
			co = int((self.x0 + WIDTH / 2) / WIDTH)
			li = int((self.y0 + HEIGHT / 2) / HEIGHT)
			self.drop(li, co)

	###################
	## Other methods ##
	###################
	
	def delete(self):
		self.canvas.delete(self.item1.get_polygon())
		self.canvas.delete(self.item2)
		self.canvas.delete(self.item3)
		
	def move(self, dx, dy):
		# Move the rectangle
		self.item1.move(dx, dy)
		# Move the letter
		(x, y) = self.canvas.coords(self.item2)
		self.canvas.coords(self.item2, (x+dx, y+dy))
		# Move the value
		(x, y) = self.canvas.coords(self.item3)
		self.canvas.coords(self.item3, (x+dx, y+dy))
		# New coordinates
		self.x0 += dx
		self.y0 += dy

	def setXY(self, x, y):
		dx = x - self.x0
		dy = y - self.y0
		self.move(dx, dy)
		
	def setLC(self, li, co):
		x = co * WIDTH
		y = li * HEIGHT
		self.setXY(x, y)
		self.li = li
		self.co = co

	def setKey(self, key):
		self.canvas.itemconfig(self.item2, text=key)
		self.key = key
		return self

	def lock(self):
		self.locked = True
	
	def askforletter(self):
		while True:
			lettre = askstring('Jocker', 'Enter a letter :', initialvalue='*', parent=self.scrabble)
			if lettre and len(lettre) == 1 and lettre.upper() in ascii_uppercase: break
		return lettre.upper()
	
	def grab(self):
		# Invoked when the tile is taken
		if self.co in range(0, 15) and self.li in range(0, 15):
			# Remove the letter from the board
			self.scrabble.get(self)
	
	def drop(self, li, co):
		# Invoked when the tile is dropped
		if co in range(0, 15) and li in range(0, 15):
			if self.scrabble.free(li, co):
				# Choice of the letter if jocker
				if self.jocker and self.key == ' ':
					self.setKey(self.askforletter())
				# Put the letter on the board
				self.scrabble.put(self, li, co)
				self.setLC(li, co)
		else:
			# The tile is dropped on the stand
			if self.jocker: self.setKey(' ')
			self.setLC(li, co)
			