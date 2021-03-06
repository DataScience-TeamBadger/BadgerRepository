# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:01:56 2017

@author: Alex Kerzner
"""

# Import config parser
from lib import Config

# Import core
from PyQt5.QtCore import Qt

# Import Qt widget components
from PyQt5.QtWidgets import \
 QApplication,\
 QMainWindow,\
 QMessageBox,\
 QWidget,\
 QPushButton,\
 QAction,\
 QTabWidget,\
 QSplitter,\
 QTreeWidget,\
 QTreeWidgetItem,\
 QStackedWidget,\
 QLabel,\
 QSpinBox,\
 QFormLayout,\
 QLineEdit,\
 QWizard,\
 QWizardPage,\
 QFileDialog,\
 QScrollArea

# Import PyQtGraph library
#import pyqtgraph as pg

# Import NumPy
#import numpy as np

# Import Core Qt components
from PyQt5.QtCore import qDebug,qInf,qWarning,qCritical,qFatal

# Import Qt main gui components
from PyQt5.QtGui import QIcon


# Import Main_Application
from Main_Application import Main_Application
from PyQt5.Qt import QDialog, QDialogButtonBox, QTextDocument, QTextBlock

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
		
		
		# Create Model Tree widget
		self.listbox = QTreeWidget()
		self.listbox.setColumnCount(1)
		self.listbox.setAnimated(True)
		self.listbox.setHeaderLabel("List of models by city")
		self.listbox.setStatusTip('Select a model')
		left_pane.addWidget(self.listbox)
		
		# Create Model Visualization widget
		self.plot = QStackedWidget()
		right_pane.addWidget(self.plot)
		
		# Create scroll area for Model Description widget
		scroll_area = QScrollArea()
		scroll_area.setWidgetResizable(True)
		left_pane.addWidget(scroll_area)
		
		# Create Model Description widget
		self.description = QLabel()
		self.description.setWordWrap(True)
		scroll_area.setWidget(self.description)
		self.description.show()
		
		
		# Add to this widget
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
Class for the about window
"""
class About_Window(QMessageBox):
	
	def __init__(self, parent):
		# Call superconstructor
		super(self.__class__, self).__init__(parent)
		self.setWindowTitle("Badger Data Science")
		text = "<h2>Badger Data Science</h2>"
		text += "<h3>Version 1.0.0</h3>"
		text += "<p>This data science project was written to analyze\
		bus and metro infrastructure in three major cities.</p>"
		text += "Created by:<ul>"
		text += "<li>mvonderlippe</li>"
		text += "<li>sproctor</li>"
		text += "<li>dsahdeo</li>"
		text += "<li>sbadger</li>"
		text += "<li>jdemey</li>"
		text += "<li>akerzner</li>"
		text += "</ul>"
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setText(text)


"""
Class for the main GUI window.
"""
class Main_Window(QMainWindow):
	
	
	"""
	Default constructor for this window.
	Calls the Main_Application
	"""
	def __init__(self):
		# Call superconstructor
		super(self.__class__, self).__init__()
		
		# Main application
		self.app = 0
		
		# Model viewer
		self.model_viewer = 0
			
		# Load configuration
		self.config = Config.getConfig()
		
		# Create application
		self.app = Main_Application()
		
		# Initialize GUI
		self.initUI()
		
		self._loadAllCities()
		
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
		self.form=form
		# Temporary value to simplify code
		current_item = ""
		
		
		
		# Set the title of the window
		self.setWindowTitle("Badger Data Science")
		
		# Resize window
		self.resize(self.config.getint("GUI", "width"),\
			self.config.getint("GUI", "height"))
		
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
		action[current_item] = QAction('&Exit', self)
		action[current_item].setShortcut('Ctrl+Shift+C')
		action[current_item].setStatusTip('Close this application')
		action[current_item].triggered.connect(self.close)
		menu["file"].addAction(action[current_item])
		
		# Create Help menu
		menu["help"] = menu_bar.addMenu('&Help')
		
		
		# Create Help->AboutQt menu
		current_item = "about_qt"
		action[current_item] = QAction('About &Qt', self)
		action[current_item].setStatusTip('About Qt')
		action[current_item].triggered.connect(QApplication.aboutQt)
		menu["help"].addAction(action[current_item])
		
		# Create Help->About menu
		current_item = "about"
		action[current_item] = QAction('&About', self)
		action[current_item].setShortcut('F1')
		action[current_item].setStatusTip('About this application')
		action[current_item].triggered.connect(self.showAboutWindow)
		menu["help"].addAction(action[current_item])
		
		
		######################
		# Create the widgets #
		######################
		
		# Create tab switcher widget
		current_item = "tab_switcher"
		widget[current_item] = QTabWidget()
		self.setCentralWidget(widget[current_item])
		widget[current_item].setStatusTip('Switch between tabs')
		
		# Create Optimize tab
		current_item = "optimize"
		tab[current_item] = QSplitter()
		tab[current_item].setStatusTip('Optimize your city')
		widget["tab_switcher"].addTab(tab[current_item], 'Optimize')
		
		# Create Predict/IO widget
		current_item = "predict_io"
		widget[current_item] = QSplitter()
		widget[current_item].setOrientation(Qt.Vertical)
		widget[current_item].setStatusTip("Predict input/output")
		tab["optimize"].addWidget(widget[current_item])
		
		# Create Predict/input layout
		layout["predict_input"] = QFormLayout()
		
		# Create Budget form input
		current_item = "budget_input"
		form.label[current_item] = QLabel()
		form.label[current_item].setText("Maximum budget (USD, thousands)")
		form.widget[current_item] = QSpinBox()
		form.widget[current_item].setSingleStep(1000)
		form.widget[current_item].setRange(1, 1000000)
		form.widget[current_item].setStatusTip("Budget, in thousands of US dollars, to allocate to your city")
		layout["predict_input"].addRow(form.label[current_item],form.widget[current_item])
		
		#Create Submit button
		current_item = "submit_button"
		form.widget[current_item] = QPushButton("Calculate")
		form.widget[current_item].clicked.connect(self.calculate)
		layout["predict_input"].addRow(form.widget[current_item])
		
		# Create Predict/output layout
		layout["predict_output"] = QFormLayout()
		
		#Create metro allocation form output
		current_item = "metro_output"
		form.label[current_item] = QLabel("Metro allocation (USD, thousands)")
		form.widget[current_item] = QLineEdit()
		form.widget[current_item].setReadOnly(True)
		form.widget[current_item].setStatusTip("Money, in thousands of US dollars, to allocate to your city's metro system")
		form.widget[current_item].setEnabled(False)
		layout["predict_output"].addRow(form.label[current_item], form.widget[current_item])
		
		#Create bus allocation form output
		current_item = "bus_output"
		form.label[current_item] = QLabel("Bus allocation (USD, thousands)")
		form.widget[current_item] = QLineEdit()
		form.widget[current_item].setReadOnly(True)
		form.widget[current_item].setEnabled(False)
		form.widget[current_item].setStatusTip("Money, in thousands of US dollars, to allocate to your city's bus system")
		layout["predict_output"].addRow(form.label[current_item], form.widget[current_item])
		
		#Create projected ridership form output
		current_item = "ridership_output"
		form.label[current_item] = QLabel("Projected ridership")
		form.widget[current_item] = QLineEdit()
		form.widget[current_item].setReadOnly(True)
		form.widget[current_item].setEnabled(False)
		form.widget[current_item].setStatusTip("How many people are expected to be transported by your transit system")
		layout["predict_output"].addRow(form.label[current_item], form.widget[current_item])
		
		# Create Predict/input widget
		current_item = "predict_input"
		widget[current_item] = QWidget()
		widget[current_item].setLayout(layout[current_item])
		widget["predict_io"].addWidget(widget[current_item])
		
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
		
	"""
	Gets called when the calculate button is pressed.
	"""
	def calculate(self):
		# Predict the values given the budget input
		if (self.form.widget['budget_input'].value() == 0):
			qWarning("Warning: a budget of zero was attempted. Action denied.")
			return
		
		goods = self.app.getTheGoods(self.form.widget['budget_input'].value())
		# Goods: $metro, $bus, $ridership
		
		# Set label for metro allocation output
		self.form.widget["metro_output"].setText(str(goods[0]))
		
		# Set label for bus allocation output
		self.form.widget["bus_output"].setText(str(goods[1]))
		
		# Set label for projected ridership output
		self.form.widget["ridership_output"].setText(str(goods[2]))
	"""
	Show about window
	"""
	def showAboutWindow(self):
		# Create about window, and show
		About_Window(self).exec_()
	
	"""
	Add a city
	"""
	def addCity(self):
		return
	
	"""
	Add UI item for a city by its id
	@param city_id the id of the city
	"""
	def _addCityItem(self, city_id):
		# Add top-level-entry for city
		city_container = QTreeWidgetItem(self.model_viewer.listbox)
		# Add name
		city_container.setText(0, self.app.cities[city_id].name)
		
		# Add all models under city
		for model_name in self.app.cities[city_id].model_names:
			model_item = QTreeWidgetItem(city_container)
			model_item.setText(0, model_name)
			self.model_viewer.plot.addWidget(self.app.cities[city_id].models[model_name].plot)
		self.model_viewer.listbox.addTopLevelItem(city_container)
	"""
	Load all cities
	"""
	def _loadAllCities(self):
		for city_id in range(len(self.app.cities)):
			self._addCityItem(city_id)
	
	"""
	GUI: Switch from previously selected model to the current selected model
	
	@param current = the current selected model
	@param previous = the previous valid selected model
	"""
	def switchModel(self, current, previous):
		# Verify that current is valid: current has no children
		if (current.childCount() == 0 and not current.parent() == None):
			# Model is selected
			city_name = current.parent().text(0)
			city_id = self.app.getCityID(city_name)
			
			if (city_id == None):
				# Redundant fail, invalid id
				print("Error: invalid selection (city id not valid)")
				return
			current_model = current.text(0)
			
			# Update plot
			self.model_viewer.plot.setCurrentWidget(self.app.cities[city_id].models[current_model].plot)
			# Update description
			self.model_viewer.description.setText(self.app.cities[city_id].models[current_model].description)
		
		# Old code
		#self.widget["plot"].plot(self.model[model_name].getX(), self.model[model_name].getY(), pen=None, symbol='o')
