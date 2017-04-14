# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:01:56 2017

@author: Alex Kerzner
"""

# Import system library
import sys

# Import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

# Class for main window
class Main_Window(QMainWindow):
	
	# Mandatory initialization - calls initialize()
	def __init__(self):
		super(self.__class__, self).__init__()
		self.initialize()
	
	# Construct GUI elements
	def initialize(self):
		self.resize(640, 480)
		self.show()
	

# 
if (__name__ == "__main__"):
	app = QApplication(sys.argv)
	mw = Main_Window()
	sys.exit(app.exec_())
