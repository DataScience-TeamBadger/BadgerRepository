# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:04:06 2017

@author: jd
"""

# Import NumPy
import numpy as np

# Import PyQtGraph library
import pyqtgraph as pg

# Import Model superclass
import Model


class TimeVsBRidership(Model.Model):
	
	def __init__(self, modelname, bus_time, bus_ridership):
		
		#Fix formatting of time to make it recognizable by numpy
		btime = []
		for i in range(len(bus_time)):
			btime.append(int(i))
     
    		# Use superclass constructor to set name and generate default plot
		super(TimeVsBRidership, self).__init__(modelname, btime, bus_ridership)
		
		# Generate X and Y
		self.X = np.asarray(btime)
		self.Y = np.asarray(bus_ridership)
		
		# Plot
		self.plot.plot(self.X, self.Y, pen=None, symbol='o')
