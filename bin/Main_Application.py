# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:39:19 2017

@author: Alex Kerzner
"""

# Import models
from models import Scatter_Model
import resources
from City import City




"""
This is the Main Application class used by the GUI.

"""
class Main_Application(object):

	# List of names of available models
    model_names = []

	# Dictionary of available models
    models = {}


    def __init__(self):
        self.cities = []
        self.test_city = City(1, "New York City", "nyc_metro.csv" ,"nyc_bus.csv")
        self.cities.append(self.test_city)
        self.gen_models()

    def gen_models(self):
        for city in self.cities:
            city_model_list = city.createModels()
            for model in city_model_list:
                new_model = model
                self.model_names.append(new_model.getName())
                self.models[new_model.getName()] = new_model






