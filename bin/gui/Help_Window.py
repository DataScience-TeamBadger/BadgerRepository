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
 QAction,\
 QGraphicsWidget,\
 QGraphicsView,\
 QGridLayout,\
 QTabWidget

# Import PyQtGraph library
import pyqtgraph as pg

# Import NumPy
import numpy as np



# Import Qt main gui components
from PyQt5.QtGui import QIcon


# Class for main window
class Main_Window(QMainWindow):
	
	# Store all menues for this window in a dictionary
	menu = {}
	
	# Store all actions for this window in a dictionary
	action = {}
	
	# Central widget
	central_widget = 0
	
	# Central layout
	#central_layout = 0
	
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
		self.action["exit"].setStatusTip('Close this application')
		self.action["exit"].triggered.connect(self.close)
		self.menu["file"].addAction(self.action["exit"])
		
		# Create and add help menu
		self.menu["help"] = menu_bar.addMenu('&Help')
		
		# Add about action to file menu
		self.action["about"] = QAction(QIcon('exit.png'), '&Exit', self)
		self.action["about"].setShortcut('F1')
		self.action["about"].setStatusTip('About this application')
		#self.action["about"].triggered.connect()
		self.menu["help"].addAction(self.action["about"])
		
		# Create status bar
		self.statusBar()
		
		# Set the central widget
		self.central_widget = QWidget()
		self.setCentralWidget(self.central_widget)
		self.central_widget.setStatusTip('Central widget')

		self.show()
	

# 
if (__name__ == "__main__"):
	app = 0
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	mw = Main_Window()
	
	# Results in an exception in IPython
	sys.exit(app.exec_())
