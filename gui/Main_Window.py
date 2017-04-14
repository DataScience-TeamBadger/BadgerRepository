# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:01:56 2017

@author: Alex Kerzner
"""

# Import system library
import sys

# Import Qt widget components
from PyQt5.QtWidgets import \
 QApplication,\
 QMainWindow,\
 QWidget,\
 QPushButton,\
 QAction

# Import Qt main gui components
from PyQt5.QtGui import QIcon


# Class for main window
class Main_Window(QMainWindow):
	
	# Store all menues for this window in a dictionary
	menu = {}
	
	# Store all actions for this window in a dictionary
	action = {}
	
	# Mandatory initialization - calls initialize()
	def __init__(self):
		super(self.__class__, self).__init__()
		self.initialize()
	
	# Construct GUI elements
	def initialize(self):
		
		# Resize and set the title of the window
		self.resize(640, 480)
		self.setWindowTitle("Badger Data Science")
		
		# Create the menu bar
		menu_bar = self.menuBar()
		
		# Create and add file menu
		self.menu["file"] = menu_bar.addMenu('&File')
		
		# Add exit action to file menu
		self.action["exit"] = QAction(QIcon('exit.png'), '&Exit', self)
		self.action["exit"].setShortcut('Ctrl+Shift+C')
		self.action["exit"].setStatusTip('Exit')
		self.action["exit"].triggered.connect(self.close)
		self.menu["file"].addAction(self.action["exit"])
		
		#button = QPushButton("Button", self)
		#button.move(100, 100)
		self.show()
	

# 
if (__name__ == "__main__"):
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	mw = Main_Window()
	
	# Results in an exception in IPython
	sys.exit(app.exec_())
