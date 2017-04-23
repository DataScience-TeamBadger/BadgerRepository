# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:39:19 2017

@author: Alex Kerzner
"""

# Import models
from models import Scatter_Model

# Import config parser
from lib import Config

"""
This is the Main Application class used by the GUI.

"""
class Main_Application(object):
	
	# List of names of available models
	model_names = []
	
	# Dictionary of available models
	models = {}
	
	"""
	Constructor for this class.
	"""
	def __init__(self):
		self.spawnRandomScatterPlots(count = 50)
	
	"""
	Demonstration
	"""
	def spawnRandomScatterPlots(self, count = 10):
		if (count < 1):
			count = 1
		# Add the specifed number of scatter plot models
		for i in range(0, count):
			# Create model
			new_model = Scatter_Model.Scatter_Model(str(i))
			self.model_names.append(new_model.getName())
			self.models[new_model.getName()] = new_model
	
	"""
	Returns the list of names of each model
	"""
	def getAllModelNames(self):
		return self.model_names
	