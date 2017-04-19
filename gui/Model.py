# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:13:37 2017

@author: Alex Kerzner
"""

# Import NumPy
import numpy as np


class Model():
	def __init__(self):
		self.X = np.empty(1)
		self.Y = np.empty(1)
	
	def setX(self, X):
		self.X = X
	
	def setY(self, Y):
		self.Y = Y
	
	def getX(self):
		return self.X
	
	def getY(self):
		return self.Y
	
	
