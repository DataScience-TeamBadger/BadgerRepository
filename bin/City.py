#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 18:51:58 2017
@author: jd
"""
import numpy as np
from models import Scatter_Model


class City():
    model_names = []
    models = {}

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

    def __init__(self, cityid, cityname, mcsv, bcsv):
        self._id = cityid
        self._name = cityname
        self._mcsv = mcsv
        self._bcsv = bcsv
        self.metro_parseCSV()
        self.bus_parseCSV()


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

    def metro_parseCSV(self):
        f = open(self._bcsv)
        f.readline()
        for line in f:
            splitline = line.split(",")
            self.metro_time.append(splitline[0])
            self.metro_ridership.append(splitline[1])
            self.metro_budget.append(splitline[2])
            self.metro_coverage.append(splitline[3])

    def createModels(self):
        new_model = Scatter_Model.Scatter_Model(str("New Model Test"))
        self.model_names.append(new_model.getName())
        self.models[new_model.getName()] = new_model

    def get_model_names(self):
        return self.model_names