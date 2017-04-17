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
 QTabWidget,\
 QSplitter,\
 QListWidget,\
 QListWidgetItem,\
 QGridLayout

# Import PyQtGraph library
import pyqtgraph as pg

# Import NumPy
import numpy as np


# Import Qt main gui components
from PyQt5.QtGui import QIcon

from PyQt5.QtPrintSupport import *


# Import Help_Window
import Help_Window


# Class for main window
class Main_Window(QMainWindow):
	
	# Store all menues for this window in a dictionary
	menu = {}
	
	# Store all actions for this window in a dictionary
	action = {}
	
	# Store all widgets for this window in a dictionary
	widget = {}
	
	# Store all operations
	op = {}
	
	# Mandatory initialization - calls initialize()
	def __init__(self):
		super(self.__class__, self).__init__()
		self.initialize()
	
	# Construct GUI elements
	def initialize(self):
		
		# Resize and set the title of the window
		self.resize(640, 480)
		self.setWindowTitle("Badger Data Science")
		#self.setStyleSheet(open("./style.qss", "r").read())
		
		# Create status bar
		self.statusBar()
		
		
		#######################
		# Create the menu bar #
		#######################
		
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
		
		
		######################
		# Create the widgets #
		######################
		
		# Create the central widget
		self.widget["central"] = QTabWidget()
		self.setCentralWidget(self.widget["central"])
		self.widget["central"].setStatusTip('central widget')
		
		# Add the predict tab
		self.widget["predict"] = QSplitter()
		self.widget["predict"].setStatusTip('predict widget')
		self.widget["central"].addTab(self.widget["predict"], 'Predict')
		
		# Add the visualize tab
		self.widget["visualize"] = QSplitter()
		self.widget["visualize"].setHandleWidth(2)
		self.widget["visualize"].setStatusTip('visualize widget')
		self.widget["central"].addTab(self.widget["visualize"], 'Visualize')
		
		# Add ops widget to visualize panel
		self.widget["ops"] = QListWidget()
		self.widget["ops"].setStatusTip('Operations')
		self.widget["visualize"].addWidget(self.widget["ops"])
		
		x = np.random.normal(size=1000)
		y = np.random.normal(size=1000)
		
		# Add plot widget to visualize panel
		self.widget["plot"] = pg.PlotWidget()
		self.widget["plot"].plot(x, y, pen=None, symbol='o')
		self.widget["plot"].setBackground([255,255,255,255])
		self.widget["plot"].setStatusTip('Plot')
		self.widget["visualize"].addWidget(self.widget["plot"])
		
		#button = QPushButton("Button", self)
		#button.move(100, 100)
		self.show()
	
	# Add plot
	def addPlot(self, title, plot):
		self.op[title] = QListWidgetItem(title)
		self.widget["ops"].addItem(self.op[title])
		self.op[title].setStatusTip("Hellawifno")
		#self.widget["ops"]
		self.widget["ops"].itemClicked.connect(self.close)
		return
	

# 
if (__name__ == "__main__"):
	# IPython override
	app = 0
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	mw = Main_Window()
	mw.addPlot("Hello world!", 0)
	
	# Results in an exception in IPython
	sys.exit(app.exec_())
