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
from scra_server import Serveur

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
		if arg == '-data': filename = sys.argv[i+1]
		if arg == '-port': port = int(sys.argv[i+1])

	file = __import__(filename)
	userdico = file.USERS
	serveur = Serveur(VERSION, LANG, port, userdico)

	serveur_thread = threading.Thread(target=serveur.run)
	serveur_thread.daemon = False
	serveur_thread.start()

if __name__ == '__main__':
	main()
