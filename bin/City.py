# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 21:39:15 2017

@author: chaddy
"""
# CSV file parsing 
import csv 
from PyQt5.QtCore import qDebug,qInf,qWarning,qCritical,qFatal
from datetime import datetime
from lib import MapHandler

from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier

import numpy as np
from models import ridership_vs_ridership, time_vs_ridership, coverage, Budget_Model


class City(object):
	# Format for date as parsed from CSV files
	DATE_FORMAT = "%Y-%m"
	
	def __init__(self, city_name, path_to_metro_csv, path_to_bus_csv, path_to_metro_map, path_to_bus_map):
		self.name = city_name 
		self.models = {}
		self.model_names = []
		
		# Dictionaries for CSV Lists
		self.time	   = {'metro':[],'bus':[]}
		self.ridership  = {'metro':[],'bus':[]}
		self.budget	 = {'metro':[],'bus':[]}
		self.coverage   = {'metro':[],'bus':[]}
		self.population = {'metro':[],'bus':[]}
		
		
		# Dictionaries for coverage (Things that use MapHandler)
		if not (path_to_metro_map == "null"):
			self.m_stations = MapHandler.getPoints(path_to_metro_map)
			self.b_stations = MapHandler.getPoints(path_to_bus_map)
		
		# Parsing CSV Calls
		self._parseCSV('metro',path_to_metro_csv)
		self._parseCSV('bus',path_to_bus_csv)
		
		# Create all models
		self.createModels(path_to_bus_map == "null")
		
		# Initialize sets
		self.training_set = []
		self.efficiency_set = []
		
		# ML Calls to populate sets
		self.classifier_format()
		self.get_city_avg_efficiency()
		self.classified_points = self.run_voting_classifier()
		#self.efficient_points = self.get_efficient_points()
	
	def _parseCSV(self, data_source, path_to_csv):
		with open(path_to_csv) as csv_file:
			# Read the file as a csv file 
			reader = csv.DictReader(csv_file)
			# Parse time, ridership, budget, and coverage
			for row in reader:
				for row in reader:
					self.time[data_source].append(datetime.strptime(row["YEAR-MONTH"], self.DATE_FORMAT))
					self.ridership[data_source].append(int(row["RIDERSHIP"]))
					self.budget[data_source].append(int(row["BUDGET"]))
					self.coverage[data_source].append(row["COVERAGE"])
					self.population[data_source].append(row["POPULATION"])
	
	def createModels(self, has_no_map = False):
		# Bar
		model_name = "Metro vs Bus (Ridership)"
		self.model_names.append(model_name)
		self.models[model_name] = ridership_vs_ridership.ridership_vs_ridership(model_name, self.ridership['metro'], self.ridership['bus'])
		# Bar
		model_name = "Metro vs Bus (Budget)"
		self.model_names.append(model_name)
		self.models[model_name] = Budget_Model.Budget_Model(model_name, self.budget['metro'], self.budget['bus'])
		# Scatter w/ LinRegression
		model_name = "Metro Ridership vs Time"
		self.model_names.append(model_name)
		self.models[model_name] = time_vs_ridership.time_vs_ridership(model_name, self.time['metro'], self.ridership['metro'])
		# Scatter w/ LinRegression
		model_name = "Bus Ridership vs Time"
		self.model_names.append(model_name)
		self.models[model_name] = time_vs_ridership.time_vs_ridership(model_name, self.time['bus'], self.ridership['bus'])
		if not (has_no_map):
			# Scatter w/ LinRegression
			model_name = "Metro Ridership vs Coverage(km2)"
			# Scatter w/ LinRegression
			model_name = "Bus Ridership vs Coverage(km2)"
			
			# (This may also be two separate ones but I imagined plotting each point
			# in one color for bus stations and another for metro stations, and then
			# overtop a transparent color that covers coverage area)
			
			model_name = "Metro(Coverage)"
			self.model_names.append(model_name)
			self.models[model_name] = coverage.coverage(model_name, self.m_stations)
			
			model_name = "Bus(Coverage)"
			self.model_names.append(model_name)
			self.models[model_name] = coverage.coverage(model_name, self.b_stations)
	
	# Formats the features into entries for our ML algorithm
	def classifier_format(self):
		self.training_set = []
		metro_ridership = self.ridership["metro"]
		bus_ridership = self.ridership["bus"]
		metro_budget = self.budget["metro"]
		bus_budget = self.budget["bus"]
		
		# Handle the length of metro and bus data
		data_length = {}
		
		# Populate data_length dictionary to store lengths of time data
		for method in ["metro", "bus"]:
			data_length[method] = len(self.time[method])
		
		if not (data_length["metro"] == data_length["bus"]):
			qWarning("Time data is not equal in length.")
			if (data_length["metro"] >= data_length["bus"]):
				# Use bus data length
				length = data_length["bus"]
			else:
				# Use metro data length
				length = data_length["metro"]
		else:
			# Use metro - using bus would work identically
			length = data_length["metro"]
		
		# Generates each entry for our SVM Training Set by totaling ridership
		#  and appending the nth element of each list to a row
		for i in range(length):
			# Verify that both bus and metro entries have matching time data
			if (self.time["metro"][i] == self.time["bus"][i]):
				entry = []
				ridership_metro = metro_ridership[i]
				ridership_bus = bus_ridership[i]
				ridership_total = ridership_metro + ridership_bus
				entry.append(ridership_total)
				entry.append(metro_budget[i])
				entry.append(bus_budget[i])
				self.training_set.append(np.asarray(entry))
			else:
				# Row skipped, invalid
				qWarning("Invalid entry[" + str(i) + "]=" + str(np.asarray(entry)))
		# Final Result is a list of lists where the inside list is a row of 
		#  ridership, and budget for each bus and metro
	
	# Develops Efficiency calculations to pass to our ML algorithm
	def get_city_avg_efficiency(self):
		self.efficiency_set = []
		i = 0
		for entry in self.training_set:
			qDebug("Training set entry[" + str(i) + "]="+str(entry) + " :: value=" + str(entry[0] / float(entry[1] + entry[2])))
			self.efficiency_set.append(entry[0] / float(entry[1] + entry[2]))
			i=i+1
		
	
	# Classification Method For Efficient Points
	# Sets of 3 classifiers, DecisionTreeClassifier, KNeighborsClassifier, and Gaussian Naive Bayes
	# Gets the weighted probability from each using training set
	# Highest weight provided to KNeightbors in order to classify consitent effiency models more heavily than what may be a 'fluke'
	# Outputs an array of the testing size where a 1 is a high efficiency and 0 is low efficiency
	def run_voting_classifier(self):
		dtc = DecisionTreeClassifier(max_depth=1)
		knn = KNeighborsClassifier(n_neighbors=6)
		gnb = GaussianNB()
		X = np.asarray(self.training_set)
		y = np.asarray(self.efficiency_set)
		eclf = VotingClassifier(estimators=[('dtc', dtc), ('knn', knn), ('gnb', gnb)], voting='soft', weights=[1.0, 4.0, 3.0])
		eclf = eclf.fit(X, y)
		return eclf
	#Takes in classification input from run_voting_classifier and reshapes it to a list containing tiples of (ridership, metro_budget, bus_budget)
	#Moved this method over to main app in order to do proper testing with the three cities
	
	#Partial Credit to: dwf @ http://stackoverflow.com/questions/2298390/fitting-a-line-in-3d
	def getLine(self, points):
		x, y, z = [], [], []
		for p in points:
			x.append(p[0])
			y.append(p[1])
			z.append(p[2])
		x = np.array(x)
		y = np.array(y)
		z = np.array(z)
		data = np.concatenate((x[:, np.newaxis], y[:, np.newaxis], z[:, np.newaxis]), axis=1)
		datamean = data.mean(axis=0)
		uu, dd, vv = np.linalg.svd(data - datamean)
		linepts = vv[0] * np.mgrid[-7:7:2j][:, np.newaxis]
		linepts += datamean
		# Prints 3d graph with line of best fit, used for test get rid of later
		import matplotlib.pyplot as plt
		import mpl_toolkits.mplot3d as m3d
		ax = m3d.Axes3D(plt.figure())
		ax.scatter3D(*data.T)
		ax.plot3D(*linepts.T)
		plt.show()
		return linepts
	
	# This function will return the ($Metro,$Bus,Ridership) tuple for the given budget
	def getGoods(self, budget, points):
		temp = self.getLine(points)
		x1 = temp[0][1]
		y1 = temp[0][2]
		z1 = temp[0][0]
		x2 = temp[1][1]
		y2 = temp[1][2]
		z2 = temp[1][0]
		slope = (y2 - y1) / (x2 - x1)
		offset = y1 - slope * x1
		slopez = (z2 - z1) / (y2 - y1)
		offsetz = z1 - slope * y1
		x = (-offset) / slope
		y = x * slope + offset
		z = y * slopez + offsetz
		while x + y <= budget - slope - 1:  # move along line till we find the goods
			x += 1
			y = x * slope + offset
			z = y * slopez + offsetz
		return (x, y, z)
	
	"""""
	def get_efficient_points(self):
		efficient_points = []
		for i in range(len(self.classified_points)):
			if self.classified_points[i] is 1:
				efficient_points.append(self.training_set)
		return efficient_points
	"""
