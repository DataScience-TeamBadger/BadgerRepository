#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 18:51:58 2017
@author: jd
"""
# CSV file parsing
import csv
from PyQt5.QtCore import qDebug,qInf,qWarning,qCritical,qFatal
from datetime import datetime
from lib import MapHandler
# TODO: import either fastkml or pykml for kml files?
# SUGGESTION: pykml is unhelpful, try fastkml or borrow the functionality off MapHandler's _hi_


import numpy as np
from models import ridership_vs_ridership, time_vs_ridership, coverage, Budget_Model

class City(object):
	
	# Format for date as parsed from CSV files
	DATE_FORMAT = "%Y-%m"
	
	
	"""
	City constructor
	"""
	def __init__(self, city_name, path_to_metro_csv, path_to_bus_csv, path_to_metro_map, path_to_bus_map):
		self.name = city_name
		self.models = {}
		self.model_names = []

		#Dictionaries For CSV Lists
		self.time       = {'metro':[],'bus':[]}
		self.ridership  = {'metro':[],'bus':[]}
		self.budget     = {'metro':[],'bus':[]}
		self.coverage   = {'metro':[],'bus':[]}
		self.population = {'metro':[],'bus':[]}

		#Dictionaries For Converage (Things that use MapHandler
		self.m_stations = MapHandler.getPoints(path_to_metro_map)
		self.b_stations = MapHandler.getPoints(path_to_bus_map)

		#self.c_area    = {'metro':[],'bus':[]}

		self._parseCSV('metro',1,path_to_metro_csv)
		self._parseCSV('bus',1,path_to_bus_csv)

		self.createModels()
    
    
    def getLine(self):
        x=[]
        y=[]
        z=[]
        
        for point in getSVMpoints():
            x.append(p[0])
            y.append(p[1])
            z.append(p[2])
            
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        
        data = np.concatenate((x[:, np.newaxis], 
                       y[:, np.newaxis], 
                       z[:, np.newaxis]), 
                      axis=1)
        datamean = data.mean(axis=0)
        uu, dd, vv = np.linalg.svd(data - datamean)
        linepts = vv[0] * np.mgrid[-7:7:2j][:, np.newaxis]
        linepts += datamean
        
        #Prints 3d graph with line of best fit, used for test get rid of later
        import matplotlib.pyplot as plt
        import mpl_toolkits.mplot3d as m3d

        ax = m3d.Axes3D(plt.figure())
        ax.scatter3D(*data.T)
        ax.plot3D(*linepts.T)
        plt.show()
        #
        
        return linepts


    #This method will return a list of (x=Ridership,y=$Metro,z=$Bus) points
    def getSVMpoints(self):
        return []
	
	"""
	Parse a given CSV file, given a data source and type.
	
	@param data_source = The data source i.e. 'metro','bus'
	@param data_type = An integer representing which data format is provided.
	@param path_to_csv = The full path to the CSV file
	"""
	def _parseCSV(self, data_source, data_type, path_to_csv):
		with open(path_to_csv) as csv_file:
			# Read the file as a csv file
			reader = csv.DictReader(csv_file)
			if (data_type == 1):
				# Parse time, ridership, budget, and coverage
				for row in reader:
					# Parse data
					self.time[data_source].append(datetime.strptime(row["YEAR-MONTH"], self.DATE_FORMAT))
					self.ridership[data_source].append(int(row["RIDERSHIP"]))
					self.budget[data_source].append(int(row["BUDGET"]))
					self.coverage[data_source].append(row["COVERAGE"])
					self.population[data_source].append(row["POPULATION"])
			elif (data_type == 2):
				# Another data type
				# Parse this data type
				return

	"""""
	JD I want you to follow the examples below and mimic the creation of the models below for each of the model names given.
	Steps:
	1. Give the model a name(Did that for you)
	2. Append the model name to the model_names list
	3. Make an elemen in the models dictionary as this example shows Model_Class.Model_Class(model_name, x_variable_array, y_variable_array)
		a. The Model_Class refers to the model class you will be making. named something like metro_bus_ridership_model.py for the first model
		b. So for each model name I put down add your model class and it should show up. In order to make the model class make sure it fits the constructor and fits the Qt API, Alex put some help on the slack in #samplecode
	"""""
	def createModels(self):
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

		# Scatter w/ LinRegression
		model_name = "Metro Ridership vs Coverage(km2)"
		
		# Scatter w/ LinRegression
		model_name = "Bus Ridership vs Coverage(km2)"

		# Map - Leave this one to me and Steven
		# (This may also be two seperate ones but I imagined plotting each point
		# in one color for bus stations and another for metro stations, and then
		# overtop a transparant color that covers coverage area)
		model_name = "Metro(Coverage)"
		self.model_names.append(model_name)
		self.models[model_name] = coverage.coverage(model_name, self.m_stations)

		model_name = "Bus(Coverage)"
		self.model_names.append(model_name)
		self.models[model_name] = coverage.coverage(model_name, self.b_stations)
