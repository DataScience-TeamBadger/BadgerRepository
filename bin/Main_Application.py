# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:39:19 2017

@author: Alex Kerzner, Michael vonderLippe, John deMay
"""

# Import library for parsing a configuration file
from ConfigParser import SafeConfigParser

# Import library for simplifying OS file paths
import os

# Import the City class to store groups of models as cities
from City import City


"""
This is the Main Application class used by the UI.

Functions in this class may be called via the UI.

"""
class Main_Application(object):
	
	# Initial configuration for cities
	_city_config_ = None
	
	# List of names of available models in each city
	model_names = []
	
	# List of cities
	cities = []
	
	"""
	Constructor for Main Application
	"""
	def __init__(self):
		# Initialize model types
		self.model_names.append("Ridership")
		self.model_names.append("Budget")
		
		
		# Parse city configuration file to get list of initial cities
		self._city_config_ = SafeConfigParser()
		self._city_config_.read(os.path.relpath('etc/cities.cfg'))
		for section in self._city_config_.sections():
			# Add each city, where section is the name of the city
			self.addCity(section, self._city_config_.get(section, "metro"),\
				self._city_config_.get(section, "bus"))
		#self.gen_models()
	
	"""
	Add a city given its name, metro data, and bus data.
	"""
	def addCity(self, city_name, path_to_metro_data, path_to_bus_data):
		# Append city to list of cities
		new_city = City(city_name, os.path.normpath(path_to_metro_data), os.path.normpath(path_to_bus_data))
		new_city.createModels()
		self.cities.append(new_city)
	
	"""
	Delete a city given its name.
	"""
	def delCity(self, city_name):
		# TODO: del functionality
		# Warning: you probably need to get index of city, then
		# delete city at that index.
		return
	
	"""
	Get id for given city name
	"""
	def getCityID(self, city_name):
		# Loop through all cities, looking for the city with the specified name.
		for city_id in range(len(self.cities)):
			if (self.cities[city_id].name == city_name):
				# Return id, as city name was found
				return city_id
		# The city was not found
		return None
