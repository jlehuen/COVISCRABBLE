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

import threading, sys

from utils import *
from scrabble import Scrabble

VERSION = (1,1)
LANG = 'EN' # Default language

###################
## Main function ##
###################

def main():
	banner('C O V I S C R A B B L E')

	# Checking the Python version
	if sys.version_info < (3,0):
		print('Python 3.x required')
		sys.exit(1)

	# Reading the command line args
	for i,arg in enumerate(sys.argv):
		if arg == '-fr': LANG = 'FR'
		if arg == '-en': LANG = 'EN'
		if arg == '-host': addr = sys.argv[i+1]
		if arg == '-port': port = int(sys.argv[i+1])

	# Splash screen
	splash = Tk()
	splash.title('C O V I S C R A B B L E  %d.%d' % VERSION)
	splash.resizable(False, False)
	image = PhotoImage(file='img/splash.png')
	Label(splash, image=image).pack()
	center(splash)

	# Identification dialog
	ident = Identification(splash)
	userdata = (ident.login, ident.passwd)
	splash.destroy()

	# Opening the main window
	root = Scrabble(VERSION, LANG, addr, port, userdata)
	root.after(1000, root.pool) # Start pooling for asynchronous messages
	root.mainloop()

if __name__ == '__main__':
	main()
