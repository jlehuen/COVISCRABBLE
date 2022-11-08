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

import math
from tkinter import *

def pairwise(iterable):
	# s -> (s0, s1), (s2, s3), etc.
	a = iter(iterable)
	return zip(a, a)

def pentagram(r1, x, y):
	r2 = r1 // 2.5
	polygon = []
	for i in range(5):
		x1 = x + r1 * math.cos(math.radians(54 + i * 72))
		y1 = y + r1 * math.sin(math.radians(54 + i * 72))
		x2 = x + r2 * math.cos(math.radians(90 + i * 72))
		y2 = y + r2 * math.sin(math.radians(90 + i * 72))
		polygon.append([x1,y1])
		polygon.append([x2,y2])
	return polygon

class RoundedPolygon():

	def __init__(self, canvas, tabx, taby, sharpness, **kwargs):
		# From https://stackoverflow.com/users/9139005/francisco-gomes
		if sharpness < 2: sharpness = 2
		ratioMultiplier = sharpness - 1
		ratioDividend = sharpness
		points = []
		for i in range(len(tabx)):
			points.append(tabx[i])
			points.append(taby[i])
			if i < (len(tabx)-1):
				points.append((ratioMultiplier*tabx[i] + tabx[i+1]) / ratioDividend)
				points.append((ratioMultiplier*taby[i] + taby[i+1]) / ratioDividend)
				points.append((ratioMultiplier*tabx[i+1] + tabx[i]) / ratioDividend)
				points.append((ratioMultiplier*taby[i+1] + taby[i]) / ratioDividend)
			else:
				points.append((ratioMultiplier*tabx[i] + tabx[0]) / ratioDividend)
				points.append((ratioMultiplier*taby[i] + taby[0]) / ratioDividend)
				points.append((ratioMultiplier*tabx[0] + tabx[i]) / ratioDividend)
				points.append((ratioMultiplier*taby[0] + taby[i]) / ratioDividend)
				points.append(tabx[0])
				points.append(taby[0])
		self.canvas = canvas
		self.polygon = canvas.create_polygon(points, **kwargs, smooth=TRUE)
		self.x0 = tabx[0]
		self.y0 = taby[0]

	def move(self, dx, dy):
		new_coords = []
		for x,y in pairwise(self.canvas.coords(self.polygon)):
			new_coords.append(x+dx)
			new_coords.append(y+dy)
		self.canvas.coords(self.polygon, new_coords)
		self.x0 += dx
		self.y0 += dy

	def goto(self, x, y):
		dx = x - self.x0
		dy = y - self.y0
		self.move(dx, dy)

	def get_polygon(self):
		return self.polygon

class RoundedRectangle(RoundedPolygon):

	def __init__(self, canvas, x0, y0, w, h, sharpness, **kwargs):
		tabx = [x0, x0+w, x0+w, x0]
		taby = [y0, y0, y0+h, y0+h]
		RoundedPolygon.__init__(self, canvas, tabx, taby, sharpness, **kwargs)
