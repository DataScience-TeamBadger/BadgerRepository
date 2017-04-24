# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:13:37 2017

@author: Alex Kerzner
"""

# Import NumPy
import numpy as np

# Import PyQtGraph library
import pyqtgraph as pg

class Model(object):
	
	def __init__(self, name, val_one, val_two):
		self.name = name
		self.plot = pg.PlotWidget()
		self.description = "no description"
		
		# Set white background
		self.plot.setBackground([255,255,255,255])
	
	# Returns name of plot
	def getName(self):
		return self.name
	