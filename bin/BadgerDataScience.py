# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:07:09 2017

@author: Alex Kerzner
"""

import sys
from PyQt5.QtWidgets import QApplication

# Import the Graphical User Interface
import User_Interface


# Run the application

# Run only if top-level class *assumed definition*
if (__name__ == "__main__"):
	# IPython override
	app = 0
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	mw = User_Interface.Main_Window()
	
	# Results in an exception in IPython, so removed
	#sys.exit(app.exec_())
	app.exec_()
