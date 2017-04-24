# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:04:06 2017

@author: Alex Kerzner
"""

# Import NumPy
import numpy as np

# Import PyQtGraph library
import pyqtgraph as pg

# Import Model superclass
import Model


class Scatter_Model(Model.Model):
	
	def __init__(self, name, val_one, val_two):
		# Use superclass constructor to set name and generate default plot
		super(Scatter_Model, self).__init__(name, val_one, val_two)

		# Generate X and Y
		self.X = np.asarray(val_one)
		self.Y = np.asarray(val_two)
		
		# Plot
		self.plot.plot(self.X, self.Y, pen=None, symbol='o')
	
