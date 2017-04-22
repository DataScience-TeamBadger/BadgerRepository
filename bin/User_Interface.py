# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:01:56 2017

@author: Alex Kerzner
"""

# Import core
from PyQt5.QtCore import Qt

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
 QSpinBox,\
 QFormLayout,\
 QLineEdit

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
Class for viewing models
"""
class ModelViewer(QSplitter):
	
	def __init__(self):
		# Call superconstructor
		super(self.__class__, self).__init__()
		
		# Create left pane
		left_pane = QSplitter()
		left_pane.setOrientation(Qt.Vertical)
		
		# Create right pane
		right_pane = QSplitter()
		right_pane.setOrientation(Qt.Vertical)
		
		
		# Create Model List widget
		self.listbox = QListWidget()
		self.listbox.setStatusTip('Select a model')
		left_pane.addWidget(self.listbox)
		
		# Create Model Visualization widget
		self.plot = QStackedWidget()
		right_pane.addWidget(self.plot)
		
		# Create Model Description widget
		self.description = QLabel()
		self.description.setText("This is <b>the</b> description of the model.")
		left_pane.addWidget(self.description)
		
		# Create Model Table widget (to be developed)
		self.table = QWidget()
		self.table.setStatusTip('To be created: the table')
		right_pane.addWidget(self.table)
		
		self.addWidget(left_pane)
		self.addWidget(right_pane)

"""
Class for storing form items
"""
class Form(object):
	def __init__(self):
		self.label = {}
		self.widget = {}




"""
Class for the main GUI window.
"""
class Main_Window(QMainWindow):
	
	# Main application
	app = 0
	
	model_viewer = 0
	model_names = []
	models = {}
	
	
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
		self.initUI()
		
		# Load models from application
		self.loadAllModels()
		
		# Show GUI
		self.show()
	
	"""
	Construct GUI elements
	"""
	def initUI(self):
		
		# Structures to hold various UI components
		menu = {}
		action = {}
		widget = {}
		tab = {}
		layout = {}
		
		form = Form()
		
		# Temporary value to simplify code
		current_item = ""
		
		
		
		# Resize and set the title of the window
		self.resize(640, 480)
		self.setWindowTitle("Badger Data Science")
		#self.setStyleSheet(open("./style.qss", "r").read())
		
		# Create status bar
		self.statusBar()
		
		
		#######################
		# Create the menu bar #
		#######################
		
		# Create menu bar
		menu_bar = self.menuBar()
		
		
		# Create File menu
		menu["file"] = menu_bar.addMenu('&File')
		
		# Create File->Exit menu
		current_item = "exit"
		action[current_item] = QAction(QIcon('exit.png'), '&Exit', self)
		action[current_item].setShortcut('Ctrl+Shift+C')
		action[current_item].setStatusTip('Close this application')
		action[current_item].triggered.connect(self.close)
		menu["file"].addAction(action[current_item])
		
		# Create Help menu
		menu["help"] = menu_bar.addMenu('&Help')
		
		
		# Create Help->About menu
		current_item = "about"
		action[current_item] = QAction(QIcon('exit.png'), '&Exit', self)
		action[current_item].setShortcut('F1')
		action[current_item].setStatusTip('About this application')
		#self.action["about"].triggered.connect()
		menu["help"].addAction(action[current_item])
		
		
		######################
		# Create the widgets #
		######################
		
		# Create tab switcher widget
		current_item = "tab_switcher"
		widget[current_item] = QTabWidget()
		self.setCentralWidget(widget[current_item])
		widget[current_item].setStatusTip('Tab switcher')
		
		# Create Optimize tab
		current_item = "optimize"
		tab[current_item] = QSplitter()
		tab[current_item].setStatusTip('optimize')
		widget["tab_switcher"].addTab(tab[current_item], 'Optimize')
		
		# Create Predict/IO widget
		current_item = "predict_io"
		widget[current_item] = QSplitter()
		widget[current_item].setOrientation(Qt.Vertical)
		widget[current_item].setStatusTip(current_item)
		tab["optimize"].addWidget(widget[current_item])
		
		# Create Predict/Visualize widget
		current_item = "predict_visualize"
		widget[current_item] = QWidget()
		widget[current_item].setStatusTip(current_item)
		tab["optimize"].addWidget(widget[current_item])
		
		# Create Predict/input layout
		layout["predict_input"] = QFormLayout()
		
		# Create Coverage form input
		current_item = "coverage"
		form.label[current_item] = QLabel()
		form.label[current_item].setText("Minimum coverage (km²)")
		form.widget[current_item] = QSpinBox()
		# Only applies to QSlider()
		#form.widget[current_item].setOrientation(Qt.Horizontal)
		form.widget[current_item].setRange(0, 1000)
		layout["predict_input"].addRow(form.label[current_item],form.widget[current_item])
		
		# Create People form input
		current_item = "people"
		form.label[current_item] = QLabel()
		form.label[current_item].setText("Minimum population (persons)")
		form.widget[current_item] = QSpinBox()
		# Only applies to QSlider()
		#form.widget[current_item].setOrientation(Qt.Horizontal)
		form.widget[current_item].setRange(0, 1000)
		layout["predict_input"].addRow(form.label[current_item],form.widget[current_item])
		
		# Create Budget form input
		current_item = "budget"
		form.label[current_item] = QLabel()
		form.label[current_item].setText("Maximum budget (USD, thousands)")
		form.widget[current_item] = QSpinBox()
		# Only applies to QSlider()
		#form.widget[current_item].setOrientation(Qt.Horizontal)
		form.widget[current_item].setRange(0, 1000)
		layout["predict_input"].addRow(form.label[current_item],form.widget[current_item])
		
		
		# Create Predict/input widget
		current_item = "predict_input"
		widget[current_item] = QWidget()
		widget[current_item].setLayout(layout[current_item])
		widget["predict_io"].addWidget(widget[current_item])
		
		
		# Create Predict/output layout
		layout["predict_output"] = QFormLayout()
		
		# Create Bus Ridership form output
		current_item = "bus"
		form.label[current_item] = QLabel()
		form.label[current_item].setText("Bus Ridership")
		form.widget[current_item] = QLineEdit()
		form.widget[current_item].setReadOnly(True)
		form.widget[current_item].setText("null")
		layout["predict_output"].addRow(form.label[current_item],form.widget[current_item])
		
		# Create Metro Ridership form output
		current_item = "metro"
		form.label[current_item] = QLabel()
		form.label[current_item].setText("Metro Ridership")
		form.widget[current_item] = QLineEdit()
		form.widget[current_item].setReadOnly(True)
		form.widget[current_item].setText("null")
		layout["predict_output"].addRow(form.label[current_item],form.widget[current_item])
		
		
		# Create Predict/output widget
		current_item = "predict_output"
		widget[current_item] = QWidget()
		widget[current_item].setLayout(layout[current_item])
		widget["predict_io"].addWidget(widget[current_item])
		
		
		# Create Data visualization tab
		current_item = "data_visualization"
		self.model_viewer = ModelViewer()
		# Enable model switching
		self.model_viewer.listbox.currentItemChanged.connect(\
			lambda current, previous: self.switchModel(current, previous))
		widget["tab_switcher"].addTab(self.model_viewer, 'Data Visualization')
		
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
		# Add listbox item
		item = QListWidgetItem(model_name)
		item.setStatusTip(model_name)
		self.model_viewer.listbox.addItem(item)
		
		# Add plot
		# EXPERIMENTAL: expected to be via reference, but may not be.
		self.model_viewer.plot.addWidget(self.app.models[model_name].plot)
	
	"""
	GUI: Switch from previously selected model to the current selected model
	"""
	def switchModel(self, current, previous):
		# Update plot
		self.model_viewer.plot.setCurrentWidget(self.app.models[current.text()].plot)
		
		# Update description
		self.model_viewer.description.setText(self.app.models[current.text()].description)
		
		# Old code
		#self.widget["plot"].plot(self.model[model_name].getX(), self.model[model_name].getY(), pen=None, symbol='o')
