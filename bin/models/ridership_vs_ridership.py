# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:04:06 2017

@author: Alex Kerzner
"""

# Import NumPy
import numpy as np

# Import matplotlib
import matplotlib.pyplot

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
  
          #Set up X axis
		self.X = np.arange(len(list_of_metro_data))
		width = 0.3
		"""
          #Add bars
		figure, axis = matplotlib.pyplot.subplots()
		metro_bars = axis.bar(self.X, list_of_metro_data, width, color='b')
		bus_bars = axis.bar(self.X, list_of_bus_data, width, color='y')
		
		#self.plot = matplotlib.pyplot.show()
		"""
		
          # Convert metro and bus data to numpy arrays
		self.Y = np.asarray(list_of_bus_data)
		self.Y2 = np.asarray(list_of_metro_data)
		
		# Plot X against Y
		self.plot.plot(self.X, self.Y, pen=None, symbol='o')
		self.plot.plot(self.X, self.Y2, pen=None, symbol='x')
          
	
