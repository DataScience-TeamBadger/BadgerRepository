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
    #Format for date as parsed from CSV files
    DATE_FORMAT = "%Y-%m"
    
    def __init__(self, city_name, path_to_metro_csv, path_to_bus_csv, path_to_metro_map, path_to_bus_map):
        self.name = city_name 
        self.models = {}
        self.model_names = []
        
        #Dictionaries for CSV Lists
        self.time       = {'metro':[],'bus':[]}
        self.ridership  = {'metro':[],'bus':[]}
        self.budget     = {'metro':[],'bus':[]}
        self.coverage   = {'metro':[],'bus':[]}
        self.population = {'metro':[],'bus':[]}
        
        #Dictionaries for converage (Things that use MapHandler)
        self.m_stations = MapHandler.getPoints(path_to_metro_map)
        self.b_stations = MapHandler.getPoints(path_to_bus_map)

        #Parsing CSV Calls
        self._parseCSV('metro',1,path_to_metro_csv)
        self._parseCSV('bus',1,path_to_bus_csv)

        #Call to main Model method
        self.createModels()

        #ML Calls
        self.training_set = self.classifier_format()
        self.classified_points = self.run_voting_classifier()
        #self.efficient_points = self.get_efficient_points()
        
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

    #Formats the features into entries for our ML algorithm
    def classifier_format(self):
        training_set = []
        metro_ridership = self.ridership["metro"]
        bus_ridership = self.ridership["bus"]
        metro_budget = self.budget["metro"]
        bus_budget = self.budget["bus"]

        # Generates each entry for our SVM Training Set by totaling ridership and appending the nth element of each list to a row
        for i in range(len(metro_ridership)):
            entry = []
            ridership_metro = metro_ridership[i]
            ridership_bus = bus_ridership[i]
            ridership_total = ridership_metro + ridership_bus
            entry.append(ridership_total)
            entry.append(metro_budget[i])
            entry.append(bus_budget[i])
            training_set.append(np.asarray(entry))
        # Final Result is a list of lists where the inside list is a row of ridership, and budget for each bus and metro
        return training_set

    #Developes Efficiency calculations to pass to our ML algorithm
    def get_city_avg_efficiency(self):
        efficiency_set = []
        for entry in self.training_set:
            efficiency_set.append(entry[0] / (entry[1] + entry[2]))
        return efficiency_set

    #Classification Method For Efficient Points
    #Sets of 3 classifiers, DecisionTreeClassifier, KNeighborsClassifier, and Gaussian Naive Bayes
    #Gets the weighted probability from each using training set
    #Highest weight provided to KNeightbors in order to classify consitent effiency models more heavily than what may be a 'fluke'
    #Outputs an array of the testing size where a 1 is a high efficiency and 0 is low efficiency
    def run_voting_classifier(self):
        clf1 = DecisionTreeClassifier(max_depth=1)
        clf2 = KNeighborsClassifier(n_neighbors=6)
        clf3 = GaussianNB()

        get_y = self.get_city_avg_efficiency() #in there cause yellow bar was pissing me off
        X = np.asarray(self.training_set)
        y = np.asarray(get_y)

        eclf = VotingClassifier(estimators=[('dtc', clf1), ('knn', clf2), ('gnb', clf3)], voting='soft', weights=[1, 4, 3])
        eclf = eclf.fit(X, y)
        return eclf

    #Takes in classification input from run_voting_classifier and reshapes it to a list containing tiples of (ridership, metro_budget, bus_budget)
    #Moved this method over to main app in order to do proper testing with the three cities
    """""
    def get_efficient_points(self):
        efficient_points = []
        for i in range(len(self.classified_points)):
            if self.classified_points[i] is 1:
                efficient_points.append(self.training_set)
        return efficient_points
    """
