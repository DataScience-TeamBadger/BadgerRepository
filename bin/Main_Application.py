# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:39:19 2017

@author: Alex Kerzner, Michael vonderLippe, John deMay
"""

# Import library for parsing a configuration file
from ConfigParser import SafeConfigParser


# Import config parser
from lib import Config

# Import library for simplifying OS file paths
import os

# Import the City class to store groups of models as cities
from City import City
from PyQt5.QtCore import qDebug,qInf,qWarning,qCritical,qFatal
"""
This is the Main Application class used by the UI.

Functions in this class may be called via the UI.

"""
class Main_Application(object):
	
	"""
	Constructor for Main Application
	"""
	def __init__(self):
		
		# Initialize list of cities
		self.cities = []
		# Parse city configuration file to get list of initial cities
		self._city_config_ = SafeConfigParser()
		self._city_config_.read(os.path.relpath('etc/cities.cfg'))
		
		print("Reading cities.cfg")
		for section in self._city_config_.sections():
			# Add each city, where section is the name of the city
			print("Loading city: " + section)
			print(" - metro: " + self._city_config_.get(section, "metro"))
			print(" - bus: " + self._city_config_.get(section, "bus"))
			print(" - metro_coverage: " + self._city_config_.get(section, "metromap"))
			print(" - bus_coverage: " + self._city_config_.get(section, "busmap"))
			self.addCity(section, self._city_config_.get(section, "metro"),\
				self._city_config_.get(section, "bus"),\
				self._city_config_.get(section, "metromap"),\
				self._city_config_.get(section, "busmap"))
		# TODO: Remove DEBUG:
		#self.gen_models()
		self.X_test = self.get_testing_set()
		self.predictions = self.test_trained_algorithm()
		self.efficient_predictions = self.get_efficient_points()

	
	"""
	Add a city given its name, metro data, and bus data.
	"""
	def addCity(self, city_name, path_to_metro_data,\
	 path_to_bus_data, path_to_metro_map, path_to_bus_map):
		# Append city to list of cities
		self.cities.append(City(city_name,\
			os.path.normpath(path_to_metro_data),\
			os.path.normpath(path_to_bus_data),\
			os.path.normpath(path_to_metro_map),\
			os.path.normpath(path_to_bus_map)))
	
	"""
	Delete a city given its name.
	@param city_name the name of the city
	"""
	def delCity(self, city_name):
		# TODO: del functionality
		# Warning: you probably need to get index of city, then
		# delete city at that index.
		return
	
	"""
	Get id for given city name
	@param city_name the name of the city for which to return the city_id
	"""
	def getCityID(self, city_name):
		# Loop through all cities, looking for the city with the specified name.
		for city_id in range(len(self.cities)):
			if (self.cities[city_id].name == city_name):
				# Return id, as city name was found
				return city_id
		# The city was not found
		return None

	# Combines the training set of each city into one massive testing set
	def get_testing_set(self):
		X = []
		for city in self.cities:
			for entry in city.training_set:
				X.append(entry)
		return X
	
	"""
	The method that returns recommended metro and bus budget allocations
	and predicted ridership for a given budget. The point of the application.
	"""
	def getTheGoods(self,budget):
		goods=[]
		sets = self.efficient_predictions
		i=0
		for city in self.cities:
			goods.append(city.getGoods(budget,sets[i]))
			i+=1
		x=0
		y=0
		z=0
		for g in goods:
			x+=g[0]
			y+=g[1]
			z+=g[2]
		i=len(self.cities)
		x/=i
		y/=i
		z/=i
		return (x,y,z)
	
	#Acquires the trained algorithm of each city
	#Spits out predictions of the testing set using each city's trained algorithm
	def test_trained_algorithm(self):
		trained_algorithm_set = []
		prediction_set = []
		for city in self.cities:
			trained_algorithm_set.append(city.run_voting_classifier())
		for trained in trained_algorithm_set:
			prediction_set.append(trained.predict(self.X_test))
		return prediction_set

	# Takes in classification input from run_voting_classifier and reshapes it to a list containing tiples of (ridership, metro_budget, bus_budget)
	def get_efficient_points(self):
		efficient_points = []
		for set in self.predictions:
			current_points = []
			for i in range(len(self.X_test)):
				if set[i] > 0:
					current_points.append(self.X_test[i])
			efficient_points.append(current_points)
		return efficient_points


