# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:01:56 2017

@author: Alex Kerzner
"""


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
 QStackedWidget,\
 QLabel,\
 QSlider,\
 QSpinBox

# Import PyQtGraph library
import pyqtgraph as pg

# Import NumPy
#import numpy as np

# Import Qt main gui components
from PyQt5.QtGui import QIcon

#from PyQt5.QtPrintSupport import *

# Import Main_Application
from Main_Application import Main_Application

"""
Class for the main GUI window.
"""
class Main_Window(QMainWindow):
	
	# Store all menus for this window in a dictionary
	menu = {}
	
	# Store all actions for this window in a dictionary
	action = {}
	
	# Store all widgets for this window in a dictionary
	widget = {}
	
	# Store all operations
	op = {}
	
	# Main application
	app = 0
	
	"""
	Default constructor for this window.
	Calls 
	"""
	def __init__(self):
		# Call superconstructor
		super(self.__class__, self).__init__()
		
		# Create application
		self.app = Main_Application()
		
		# Initialize GUI
		self.initializeGUI()
		
		# Load models from application
		self.loadAllModels()
		
		# Show GUI
		self.show()
	
	"""
	Construct GUI elements
	"""
	def initializeGUI(self):
		
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
		self.widget["ops"].currentItemChanged.connect(lambda current, previous: self.switchModel(current, previous))
		
		# Add plot widget to visualize panel
		self.widget["plot"] = QStackedWidget()
		self.widget["visualize"].addWidget(self.widget["plot"])
		
		#button = QPushButton("Button", self)
		#button.move(100, 100)
	
	"""
	Add all models from application
	"""
	def loadAllModels(self):
		# Add each model
		for model_name in self.app.model_names:
			self.addModel(model_name)
	
	"""
	Add model to GUI by model_name
	
	"""
	def addModel(self, model_name):
		# Add to list box
		item = QListWidgetItem(model_name)
		item.setStatusTip(model_name)
		self.widget["ops"].addItem(item)
		
		# Add model's plot widget to GUI plot widget
		# EXPERIMENTAL: expected to be via reference, but may not be.
		self.widget["plot"].addWidget(self.app.models[model_name].plot)
	
	"""
	GUI: Switch from previously selected model to the current selected model
	"""
	def switchModel(self, current, previous):
		self.widget["plot"].setCurrentWidget(self.app.models[current.text()].plot)
		
		# Old code
		#self.widget["plot"].plot(self.model[model_name].getX(), self.model[model_name].getY(), pen=None, symbol='o')
