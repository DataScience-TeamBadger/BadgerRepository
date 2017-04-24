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

"""
A model representing a comparison between Metro and Bus Budget

parameters: city_name, list_of_metro_data, list_of_bus_data
"""
class Budget_Model(Model.Model):
	
	"""
	Constructor for Budget Model
	"""
	def __init__(self, city_name, list_of_metro_data, list_of_bus_data):
		# Call superconstructor to load defaults
		super(self.__class__, self).__init__()
		self.name = city_name
		
		# Convert metro and bus data to numpy arrays
		self.X = np.asarray(list_of_metro_data)
		self.Y = np.asarray(list_of_bus_data)
		
		# Plot X against Y
		self.plot.plot(self.X, self.Y, pen=None, symbol='o')
	
