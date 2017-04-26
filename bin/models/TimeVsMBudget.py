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


class TimeVsMBudget(Model.Model):
	
	def __init__(self, modelname, metro_time, metro_budget):
		
		#Fix formatting of time to make it recognizable by numpy
		mtime = []
		for i in range(len(metro_time)):
			mtime.append(int(i))
     
    		# Use superclass constructor to set name and generate default plot
		super(TimeVsMBudget, self).__init__(modelname, mtime, metro_budget)
		
		# Generate X and Y
		self.X = np.asarray(mtime)
		self.Y = np.asarray(metro_budget)
		
		# Plot
		self.plot.plot(self.X, self.Y, pen=None, symbol='o')