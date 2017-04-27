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

import numpy as np
from models import ridership_vs_ridership, time_vs_ridership, coverage, Budget_Model


class City(object):
    #Format for date as parsed from CSV files
    DATE_FORMAT = "%Y-%m"
    
    def __init__(self, city_name, path_to_metro_csv, path_to_bus_csv, path_to_metro_map, path_to_bus_map):
        self.name = city_name 
        self.models = {}
        self.model_name = []
        
        #Dictionaries for CSV Lists
        self.time       = {'metro':[],'bus':[]}
        self.ridership  = {'metro':[],'bus':[]}
        self.budget     = {'metro':[],'bus':[]}
        self.coverage   = {'metro':[],'bus':[]}
        self.population = {'metro':[],'bus':[]}
        
        #Dictionaries for converage (Things that use MapHandler)
        self.m_stations = MapHandler.getPoints(path_to_metro_map)
        self.b_stations = MapHandler.getPoints(path_to_bus_map)
        
        self._parseCSV('metro',1,path_to_metro_csv)
        self._parseCSV('bus',1,path_to_bus_csv)
        
        self.createModels()
        self.svm_training_set = self.svm_format()
        
    def _parseCSV(self, data_source, data_type, path_to_csv):
        with open(path_to_csv) as csv_file:
            #Read the file as a csv file 
            reader = csv.DictReader(csv_file)
            if (data_type == 1):
                # Parse time, ridership, budget, and coverage
                for row in reader:
                    for row in reader:
					# Parse data
					self.time[data_source].append(datetime.strptime(row["YEAR-MONTH"], self.DATE_FORMAT))
					self.ridership[data_source].append(int(row["RIDERSHIP"]))
					self.budget[data_source].append(int(row["BUDGET"]))
					self.coverage[data_source].append(row["COVERAGE"])
					self.population[data_source].append(row["POPULATION"])
            elif (data_type == 2):
                #Another data type 
                #Parse this data type
                return
            
    def svm_format(self):
        training_set = []
        metro_ridership = self.ridership["metro"]
        bus_ridership = self.ridership["bus"]
        metro_budget = self.bus["metro"]
        bus_budget = self.bus["bus"]
        
        #Generates each entry for our SVM Training Set by totaling ridership and appending the nth element of each list to a row
        for i in range(len(metro_ridership)):
            entry = []
            ridership_metro = metro_ridership[i]
            ridership_bus = bus_ridership[i]
            ridership_total = ridership_metro + ridership_bus
            entry.append(ridership_total)
            entry.append(metro_budget[i])
            entry.append(bus_budget[i])
            training_set.append(entry)
        #Final Result is a list of lists where the inside list is a row of ridership, and budget for each bus and metro
        return training_set
    
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
                                              
        # (This may also be two seperate ones but I imagined plotting each point
        # in one color for bus stations and another for metro stations, and then
        # overtop a transparant color that covers coverage area)
        
        model_name = "Metro(Coverage)"
        self.model_names.append(model_name)
        self.models[model_name] = coverage.coverage(model_name, self.m_stations)
        
        model_name = "Bus(Coverage)"
        self.model_names.append(model_name)
        self.models[model_name] = coverage.coverage(model_name, self.b_stations)
        
                                               