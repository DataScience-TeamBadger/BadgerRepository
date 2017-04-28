# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:13:37 2017

@author: Alex Kerzner
"""

# Import NumPy
import numpy as np

# Import PyQtGraph library
import pyqtgraph as pg
"""
An abstract Model type to be implemented by every model.
This contains <b>everything</b> needed by the GUI - it is up to the
implementation of this Model to customize it.

@param name = the name of the model, or "Unnamed Model" if not provided.
"""
class Model(object):
	
	def __init__(self, name = "Unnamed Model"):
		
		# Set the name of the model
		self.name = name
		
		# Create an empty plot
		self.plot = pg.PlotWidget()
		
		# Default plot properties
		
		# Set white background
		self.plot.setBackground([255,255,255,255])
		
		
		
		
		# Create an empty description
		self.description = "<h3>Header for this empty model</h3>"
		self.description += "This model loads <b>bold</b> and <i>italics</i>.<br>"
		self.description += "Hello world!"
		
	
	# Returns name of plot
	def getName(self):
		return self.name
	