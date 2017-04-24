#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 18:51:58 2017
@author: jd
"""
import numpy as np
from models import Scatter_Model,Ridership_Model,Budget_Model

class City(object):
    
    metro_time = []
    metro_ridership = []
    metro_budget = []
    metro_coverage = []
    metro_model_names = []
    
    bus_time = []
    bus_ridership = []
    bus_budget = []
    bus_coverage = []
    bus_model_names = []
    
    def __init__(self, cityname, metro_csv, bus_csv, metro_coverage, bus_coverage):
        #self._id = cityid
        self.name = cityname
        self._mcsv = metro_csv
        self._bcsv = bus_csv
        self.metro_parseCSV()
        self.bus_parseCSV()
        self.models = {}
        self.model_names = []
        self.createModels()

    # parsecsvintonparrays()
    # createModel(np1, np2)
    
    def bus_parseCSV(self):
        f = open(self._mcsv)
        f.readline()
        for line in f:
            splitline = line.split(",")
            self.bus_time.append(splitline[0])
            self.bus_ridership.append(splitline[1])
            self.bus_budget.append(splitline[2])
            self.bus_coverage.append(splitline[3])
        f.close()
    
    def metro_parseCSV(self):
        f = open(self._bcsv)
        f.readline()
        for line in f:
            splitline = line.split(",")
            self.metro_time.append(splitline[0])
            self.metro_ridership.append(splitline[1])
            self.metro_budget.append(splitline[2])
            self.metro_coverage.append(splitline[3])
        f.close()
    
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
        model_name = "Metro vs Bus (Ridership)" #Bar
        self.model_names.append(model_name)
        self.models[model_name] = Ridership_Model.Ridership_Model(model_name,self.metro_ridership, self.bus_ridership)
        model_name = "Metro vs Bus (Budget)" #Bar
        self.model_names.append(model_name)
        self.models[model_name] = Budget_Model.Budget_Model(model_name,self.metro_budget, self.bus_budget)
        model_name = "Metro vs Bus (Coverage)" #Map Leave this one to me and Steven(This may also be two seperate ones but I imagined plotting each point in one color for bus stations and another for metro stations, and then overtop a transparant color that covers coverage area)
        model_name = "Metro Ridership vs Time" #Scatter w/ LinRegression
        model_name = "Bus Ridership vs Time"    #Scatter w/ LinRegression
        model_name = "Metro Ridership vs Coverage(km2)" #Scatter w/ LinRegression
        model_name = "Bus Ridership vs Coverage(km2)" #Scatter w/ LinRegression

    # unnecessary - city.model_names from outside
    def get_model_names(self):
        return self.model_names
    # unnecessary - city.models from outside.
    def get_models(self):
        return self.models
