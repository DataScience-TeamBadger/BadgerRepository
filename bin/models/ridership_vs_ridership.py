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
import models.Model

"""
A model representing a comparison between Metro and Bus Ridership

parameters: city_name, list_of_metro_data, list_of_bus_data
"""
class ridership_vs_ridership(models.Model.Model):
	
	"""
	Constructor for Ridership Model
	"""
	def __init__(self, city_name, list_of_metro_data, list_of_bus_data):
		# Call superconstructor to load defaults
		super(self.__class__, self).__init__()
		self.name = city_name
		self.description = "<h3>Ridership vs Ridership</h3>"
		self.description +="<h5>X-Axis = Time</h5>"
		self.description +="<h5>Y-Axis = Ridership</h5>"
		self.description +="<h5>x = Metro</h5>"
		self.description +="<h5>o = Bus</h5>"
		# Convert metro and bus data to numpy arrays
		self.X = np.asarray(list_of_metro_data)
		self.Y = np.asarray(list_of_bus_data)
		
		# Plot X against Y
		self.plot.plot(self.X, self.Y, pen=None, symbol='o')
	
