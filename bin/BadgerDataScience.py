# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:07:09 2017

@author: Alex Kerzner
"""



import sys
from PyQt5.QtWidgets import QApplication

# Import the Graphical User Interface
import User_Interface

# Import config parser
from lib import Config

# Run the application

# Don't run if loaded as module
if (__name__ == "__main__"):
	
	config = Config.getConfig()
	
	
	# IPython override
	app = 0
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	mw = User_Interface.Main_Window()
	
	
	# Results in an exception in IPython, so removed
	#sys.exit(app.exec_())
	app.exec_()
