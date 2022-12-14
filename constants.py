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

WIDTH = 40 # Default width of the tiles

HEIGHT = WIDTH * 1.1
BOARD_WIDTH = WIDTH * 15
BOARD_HEIGHT = HEIGHT * 15
STAND_HEIGHT = HEIGHT * 3
TOTAL_HEIGHT = BOARD_HEIGHT + STAND_HEIGHT

COLOR_BLUE1 = '#%02X%02X%02X' % (180, 200, 210)
COLOR_BLUE2 = '#%02X%02X%02X' % (90, 150, 180)
COLOR_RED1 = '#%02X%02X%02X' % (240, 190, 170)
COLOR_RED2 = '#%02X%02X%02X' % (240, 110, 80)
COLOR_NONE = '#%02X%02X%02X' % (220, 220, 200)
COLOR_LINE = '#%02X%02X%02X' % (0, 150, 0)

# https://en.wikipedia.org/wiki/Scrabble_letter_distributions

BAG_FR = {
	'A':(1,9), 'B':(3,2), 'C':(3,2), 'D':(2,3), 'E':(1,15), 'F':(4,2), 'G':(2,2),
	'H':(4,2), 'I':(1,8), 'J':(8,1), 'K':(10,1), 'L':(1,5), 'M':(2,3), 'N':(1,6),
	'O':(1,6), 'P':(3,2), 'Q':(8,1), 'R':(1,6), 'S':(1,6), 'T':(1,6), 'U':(1,6),
	'V':(4,2), 'W':(10,1), 'X':(10,1), 'Y':(10,1), 'Z':(10,1), ' ':(0,2) }

BAG_EN = {
	'A':(1,9), 'B':(3,2), 'C':(3,2), 'D':(2,4), 'E':(1,12), 'F':(4,2), 'G':(2,3),
	'H':(4,2), 'I':(1,9), 'J':(8,1), 'K':(5,1), 'L':(1,4), 'M':(2,3), 'N':(1,6),
	'O':(1,8), 'P':(3,2), 'Q':(10,1), 'R':(1,6), 'S':(1,4), 'T':(1,6), 'U':(1,4),
	'V':(4,2), 'W':(4,2), 'X':(8,1), 'Y':(4,2), 'Z':(10,1), ' ':(0,2) }

BOARD_VAL1 = [
	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1],
	[1,1,1,1,1,3,1,1,1,3,1,1,1,1,1],
	[1,1,1,1,1,1,2,1,2,1,1,1,1,1,1],
	[2,1,1,1,1,1,1,2,1,1,1,1,1,1,2],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
	[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1],
	[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
	[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[2,1,1,1,1,1,1,2,1,1,1,1,1,1,2],
	[1,1,1,1,1,1,2,1,2,1,1,1,1,1,1],
	[1,1,1,1,1,3,1,1,1,3,1,1,1,1,1],
	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1]]

BOARD_VAL2 = [
	[3,1,1,1,1,1,1,3,1,1,1,1,1,1,3],
	[1,2,1,1,1,1,1,1,1,1,1,1,1,2,1],
	[1,1,2,1,1,1,1,1,1,1,1,1,2,1,1],
	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1],
	[1,1,1,1,2,1,1,1,1,1,2,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[3,1,1,1,1,1,1,2,1,1,1,1,1,1,3],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,2,1,1,1,1,1,2,1,1,1,1],
	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1],
	[1,1,2,1,1,1,1,1,1,1,1,1,2,1,1],
	[1,2,1,1,1,1,1,1,1,1,1,1,1,2,1],
	[3,1,1,1,1,1,1,3,1,1,1,1,1,1,3]]
