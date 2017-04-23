# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:07:09 2017

@author: Alex Kerzner
"""


import ConfigParser

import sys
from PyQt5.QtWidgets import QApplication

# Import the Graphical User Interface
import User_Interface


# Run the application

# Run only if top-level class *assumed definition*
if (__name__ == "__main__"):
	
	config = ConfigParser.SafeConfigParser()
	
	# Load default settings
	config.read('defaults.cfg')
	
	# Load custom settings, if defined
	config.read('settings.cfg')
	
	
	
	# IPython override
	app = 0
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	mw = User_Interface.Main_Window()
	
	# Resize window
	mw.resize(config.getint("GUI", "width"),config.getint("GUI", "height"))
	
	
	# Results in an exception in IPython, so removed
	#sys.exit(app.exec_())
	app.exec_()
